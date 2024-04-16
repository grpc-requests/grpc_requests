import multiprocessing
import time

import pytest
from test_servers.client_tester.client_tester_server import ClientTesterServer
from test_servers.dependencies.dependencies_server import (
    HelloWorldServer as DependencyServer,
)
from test_servers.helloworld.helloworld_server import HelloWorldServer
from tests.test_servers.helloworld.helloworld_server import EmptyGreeter


def helloworld_server_starter():
    server = HelloWorldServer("50051")
    server.serve()


def client_tester_server_starter():
    server = ClientTesterServer("50052")
    server.serve()


def dependency_server_starter():
    server = DependencyServer("50053")
    server.serve()


def helloworld_empty_server_starter():
    server = HelloWorldServer("50054", servicer=EmptyGreeter())
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


@pytest.fixture(scope="session", autouse=True)
def dependency_server():
    dependency_server_process = multiprocessing.Process(
        target=dependency_server_starter
    )
    dependency_server_process.start()
    time.sleep(1)
    yield
    dependency_server_process.terminate()


@pytest.fixture(scope="session", autouse=True)
def helloworld_empty_server():
    helloworld_empty_server_process = multiprocessing.Process(
        target=helloworld_empty_server_starter
    )
    helloworld_empty_server_process.start()
    time.sleep(1)
    yield
    helloworld_empty_server_process.terminate()
