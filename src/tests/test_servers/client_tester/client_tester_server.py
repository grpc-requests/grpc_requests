from concurrent import futures
from grpc_reflection.v1alpha import reflection

import grpc
import logging
from .client_tester_pb2_grpc import (
    ClientTesterServicer,
    add_ClientTesterServicer_to_server,
)
from .client_tester_pb2 import TestResponse, DESCRIPTOR


class ClientTester(ClientTesterServicer):
    def TestUnaryUnary(self, request, context):
        return TestResponse(average=0.0, feedback="Acceptable")

    def TestUnaryStream(self, request, context):
        for _ in request.readings:
            yield TestResponse(average=0.0, feedback="Acceptable")

    def TestStreamUnary(self, request_iterator, context):
        for _ in request_iterator:
            pass
        return TestResponse(average=0.0, feedback="Acceptable")

    def TestStreamStream(self, request_iterator, context):
        for request in request_iterator:
            for _ in request.readings:
                yield TestResponse(average=0.0, feedback="Acceptable")


class ClientTesterServer:
    server = None

    def __init__(self, port: str):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_ClientTesterServicer_to_server(ClientTester(), self.server)
        SERVICE_NAMES = (
            DESCRIPTOR.services_by_name["ClientTester"].full_name,
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
    server = ClientTesterServer("50051")
    server.serve()
