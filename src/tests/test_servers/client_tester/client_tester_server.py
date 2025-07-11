from concurrent import futures
from grpc_reflection.v1alpha import reflection

import grpc
import logging
from .client_tester_pb2_grpc import (
    ClientTesterServicer,
    add_ClientTesterServicer_to_server,
)
from .client_tester_pb2 import TestResponse, DESCRIPTOR

import os


def _load_credential_from_file(filepath):
    real_path = os.path.join(os.path.dirname(__file__), filepath)
    with open(real_path, "rb") as f:
        return f.read()

SERVER_CERTIFICATE = _load_credential_from_file("../credentials/localhost.pem")
SERVER_CERTIFICATE_KEY = _load_credential_from_file("../credentials/localhost-key.pem")


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

    def __init__(self, port: str, secure_port: str):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_ClientTesterServicer_to_server(ClientTester(), self.server)
        SERVICE_NAMES = (
            DESCRIPTOR.services_by_name["ClientTester"].full_name,
            reflection.SERVICE_NAME,
        )
        logging.debug(f"Key {SERVER_CERTIFICATE_KEY}, Server Certificate {SERVER_CERTIFICATE}")
        reflection.enable_server_reflection(SERVICE_NAMES, self.server)
        self.server.add_insecure_port(f"[::]:{port}")
        self.server.add_secure_port(f"[::]:{secure_port}", grpc.ssl_server_credentials([(SERVER_CERTIFICATE_KEY, SERVER_CERTIFICATE)], require_client_auth=False))

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
    logging.basicConfig(level=logging.DEBUG)
    server = ClientTesterServer("50051", "50052")
    server.serve()
