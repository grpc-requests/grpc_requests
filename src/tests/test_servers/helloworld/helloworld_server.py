from concurrent import futures
from grpc_reflection.v1alpha import reflection

import grpc
import logging
from .helloworld_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from .helloworld_pb2 import HelloReply, DESCRIPTOR

class Greeter(GreeterServicer):

    def SayHello(self, request, context):
        """
        Unary-Unary
        Sends a HelloReply based on a HelloRequest.
        """
        authorized = False
        if context.invocation_metadata():
            for key, value in context.invocation_metadata():
                if key == "password" and value == "12345":
                    authorized = True

        if authorized:
            return HelloReply(message=f"Hello, {request.name}, password accepted!")
        else:
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
        names = []
        for request in request_iterator:
            names.append(request.name)
        names_string = " ".join(names)
        return HelloReply(message=f"Hello, {names_string}!")

    def SayHelloOneByOne(self, request_iterator, context):
        """
        Stream-Stream
        Streams HelloReplies in response to a stream of HelloRequests.
        """
        for request in request_iterator:
            yield HelloReply(message=f"Hello {request.name}")


class HelloWorldServer():

    server = None

    def __init__(self, port: str):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_GreeterServicer_to_server(Greeter(), self.server)
        SERVICE_NAMES = (
            DESCRIPTOR.services_by_name['Greeter'].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, self.server)
        self.server.add_insecure_port(f'[::]:{port}')

    def serve(self):
        logging.debug('Server starting...')
        self.server.start()
        logging.debug('Server running...')
        self.server.wait_for_termination()

    def shutdown(self):
        self.server.stop(grace=3)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()


if __name__ == "__main__":
    server = HelloWorldServer("50051")
    server.serve()
