import multiprocessing
import pytest
import time

from test_servers.helloworld.helloworld_server import HelloWorldServer
from test_servers.client_tester.client_tester_server import ClientTesterServer


def helloworld_server_starter():
    server = HelloWorldServer("50051")
    server.serve()


def client_tester_server_starter():
    server = ClientTesterServer("50052")
    server.serve()


@pytest.fixture(scope="session", autouse=True)
def helloworld_server():
    helloworld_server_process = multiprocessing.Process(
        target=helloworld_server_starter
    )
    helloworld_server_process.start()
    time.sleep(1)
    yield
    helloworld_server_process.terminate()


@pytest.fixture(scope="session", autouse=True)
def client_tester_server():
    client_tester_server_process = multiprocessing.Process(
        target=client_tester_server_starter
    )
    client_tester_server_process.start()
    time.sleep(1)
    yield
    client_tester_server_process.terminate()
