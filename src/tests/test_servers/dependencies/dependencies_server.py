from concurrent import futures
from grpc_reflection.v1alpha import reflection

import grpc
import logging

from .dependencies_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from .dependencies_pb2 import HelloReply, DESCRIPTOR
from .dependency1_pb2 import Dependency1
from .dependency2_pb2 import Dependency2


class Greeter(GreeterServicer):
    def SayHello(self, request, context):
        """
        Unary-Unary
        Sends a HelloReply based on a HelloRequest.
        """
        if context.invocation_metadata():
            for key, value in context.invocation_metadata():
                if key == "password" and value == "12345":
                    return HelloReply(
                        message=f"Hello, {request.name}, password accepted!"
                    )
                if key == "interceptor" and value == "true":
                    return HelloReply(
                        message=f"Hello, {request.name}, interceptor accepted!"
                    )
        return HelloReply(message=f"Hello, {request.name}!")

    def SayHelloGroup(self, request, context):
        """
        Unary-Stream
        Streams a series of HelloReplies based on the names in a HelloRequest.
        """
        names = request.name
        for name in names.split():
            yield HelloReply(message=f"Hello, {name}!")

    def HelloEveryone(self, request_iterator, context):
        """
        Stream-Unary
        Sends a HelloReply based on the name recieved from a stream of
        HelloRequests.
        """
        names = [request.name for request in request_iterator]
        names_string = " ".join(names)
        return HelloReply(message=f"Hello, {names_string}!")

    def SayHelloOneByOne(self, request_iterator, context):
        """
        Stream-Stream
        Streams HelloReplies in response to a stream of HelloRequests.
        """
        for request in request_iterator:
            yield HelloReply(message=f"Hello {request.name}")

    def HasDependencies(self, request, context):
        """
        Unary-Unary
        Sends a HelloReply based on a HelloRequest.
        """
        return Dependency1(field2=Dependency2)


class HelloWorldServer:
    server = None

    def __init__(self, port: str):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_GreeterServicer_to_server(Greeter(), self.server)
        SERVICE_NAMES = (
            DESCRIPTOR.services_by_name["Greeter"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, self.server)
        self.server.add_insecure_port(f"[::]:{port}")

    def serve(self):
        logging.debug("Server starting...")
        self.server.start()
        logging.debug("Server running...")
        self.server.wait_for_termination()

    def shutdown(self):
        self.server.stop(grace=3)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()


if __name__ == "__main__":
    server = HelloWorldServer("50053")
    server.serve()
