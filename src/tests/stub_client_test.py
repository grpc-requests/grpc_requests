import logging
import pytest

from grpc_requests.client import StubClient
from test_servers.helloworld.helloworld_pb2 import _GREETER
from google.protobuf.json_format import ParseError

"""
Test cases for reflection based client
"""

logger = logging.getLogger("name")


@pytest.fixture(scope="module")
def helloworld_stub_client():
    try:
        client = StubClient("localhost:50051", [_GREETER])
        yield client
    except:  # noqa: E722
        pytest.fail("Could not connect to local HelloWorld server")


def test_unary_unary(helloworld_stub_client):
    response = helloworld_stub_client.unary_unary(
        "helloworld.Greeter", "SayHello", {"name": "sinsky"}
    )
    assert isinstance(response, dict)
    assert response == {"message": "Hello, sinsky!"}


def test_empty_body_request(helloworld_stub_client):
    response = helloworld_stub_client.unary_unary("helloworld.Greeter", "SayHello", {})
    logger.warning(f"Response: {response}")
    assert isinstance(response, dict)


def test_nonexistent_service(helloworld_stub_client):
    with pytest.raises(ValueError):
        helloworld_stub_client.unary_unary("helloworld.Speaker", "SingHello", {})


def test_nonexistent_method(helloworld_stub_client):
    with pytest.raises(ValueError):
        helloworld_stub_client.unary_unary("helloworld.Greeter", "SayGoodbye", {})


def test_unsupported_argument(helloworld_stub_client):
    with pytest.raises(ParseError):
        helloworld_stub_client.unary_unary(
            "helloworld.Greeter", "SayHello", {"foo": "bar"}
        )


def test_unary_stream(helloworld_stub_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    responses = helloworld_stub_client.unary_stream(
        "helloworld.Greeter", "SayHelloGroup", {"name": "".join(name_list)}
    )
    assert all(isinstance(response, dict) for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello, {name}!"}


def test_stream_unary(helloworld_stub_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    response = helloworld_stub_client.stream_unary(
        "helloworld.Greeter", "HelloEveryone", [{"name": name} for name in name_list]
    )
    assert isinstance(response, dict)
    assert response == {"message": f'Hello, {" ".join(name_list)}!'}


def test_stream_stream(helloworld_stub_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    responses = helloworld_stub_client.stream_stream(
        "helloworld.Greeter", "SayHelloOneByOne", [{"name": name} for name in name_list]
    )
    assert all(isinstance(response, dict) for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello, {name}!"}
