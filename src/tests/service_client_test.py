import logging
import pytest

from grpc_requests.client import Client, ServiceClient

"""
Test cases for ServiceClient
"""

logger = logging.getLogger("name")


@pytest.fixture(scope="module")
def helloworld_service_client():
    try:
        client = ServiceClient(Client("localhost:50051"), "helloworld.Greeter")
        yield client
    except:  # noqa: E722
        pytest.fail("Could not connect to local HelloWorld server")


def test_method_names(helloworld_service_client):
    method_names = helloworld_service_client.method_names
    assert method_names == (
        "SayHello",
        "SayHelloGroup",
        "HelloEveryone",
        "SayHelloOneByOne",
    )
