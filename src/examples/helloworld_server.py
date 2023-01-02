from concurrent import futures
from grpc_reflection.v1alpha import reflection

import grpc
import helloworld_proto.helloworld_pb2_grpc
import helloworld_proto.helloworld_pb2
import sys

import logging

stdout_handler = logging.StreamHandler(stream=sys.stdout)

formatter = logging.Formatter()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s : %(name)s : %(message)s',
    handlers=[stdout_handler]
)

logger = logging.getLogger(__name__)


class Greeter(helloworld_proto.helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        """
        Unary-Unary
        Sends a HelloReply based on a HelloRequest.
        """
        logger.info(f"SayHello received request: {request}.")
        return helloworld_proto.helloworld_pb2.HelloReply(message=f"Hello, {request.name}!")

    def SayHelloGroup(self, request, context):
        """
        Unary-Stream
        Streams a series of HelloReplies based on the names in a HelloRequest.
        """
        logger.info("SayHelloGroup received request.")
        names = request.name
        for name in names.split():
            yield helloworld_proto.helloworld_pb2.HelloReply(message=f"Hello, {name}!")

    def HelloEveryone(self, request_iterator, context):
        """
        Stream-Unary
        Sends a HelloReply based on the name recieved from a stream of
        HelloRequests.
        """
        logger.info("HelloEveryone received request.")
        names = []
        for request in request_iterator:
            logger.info(request.name)
            names.append(request.name)
            logger.info(names)
        names_string = " ".join(names)
        return helloworld_proto.helloworld_pb2.HelloReply(message=f"Hello, {names_string}!")

    def SayHelloOneByOne(self, request_iterator, context):
        """
        Stream-Stream
        Streams HelloReplies in response to a stream of HelloRequests.
        """
        logger.info("SayHelloOneByOne received request.")
        for request in request_iterator:
            yield helloworld_proto.helloworld_pb2.HelloReply(message=f"Hello {request.name}")


def serve():
    logger.info("Configuring Helloworld Server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_proto.helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    SERVICE_NAMES = (
        helloworld_proto.helloworld_pb2.DESCRIPTOR.services_by_name['Greeter'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    logger.info("Reflection Enabled for Helloworld Server")
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("Helloworld Server running on port 50051")
    server.wait_for_termination()
    logger.info("Helloworld Server shutting down.")


if __name__ == '__main__':
    serve()
