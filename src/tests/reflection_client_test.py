import logging
import pytest

from grpc_requests.client import Client
from google.protobuf.json_format import ParseError

from tests.common import MetadataClientInterceptor

"""
Test cases for reflection based client
"""

logger = logging.getLogger('name')

@pytest.fixture(scope="module")
def helloworld_reflection_client():
    try:
        client = Client.get_by_endpoint('localhost:50051')
        yield client
    except:  # noqa: E722
        pytest.fail("Could not connect to local HelloWorld server")

@pytest.fixture(scope="module")
def helloworld_reflection_client_with_interceptor():
    try:
        # Don't use get_by_endpoint here, because interceptors are not cached. Consider caching kwargs too
        client = Client('localhost:50051', interceptors=[MetadataClientInterceptor()])
        yield client
    except:  # noqa: E722
        pytest.fail("Could not connect to local HelloWorld server")

@pytest.fixture(scope="module")
def client_tester_reflection_client():
    try:
        client = Client.get_by_endpoint('localhost:50051')
        yield client
    except:  # noqa: E722
        pytest.fail("Could not connect to local Test server")

def test_metadata_usage(helloworld_reflection_client):
    response = helloworld_reflection_client.request(
        'helloworld.Greeter', 'SayHello',
        {"name": "sinsky"},
        metadata=[('password', '12345')]
    )
    assert isinstance(response, dict)
    assert response == {"message": "Hello, sinsky, password accepted!"}

def test_interceptor_usage(helloworld_reflection_client_with_interceptor):
    response = helloworld_reflection_client_with_interceptor.request(
        'helloworld.Greeter', 'SayHello',
        {"name": "sinsky"},
    )
    assert isinstance(response, dict)
    assert response == {"message": "Hello, sinsky, interceptor accepted!"}


def test_unary_unary(helloworld_reflection_client):
    response = helloworld_reflection_client.request('helloworld.Greeter', 'SayHello', {"name": "sinsky"})
    assert isinstance(response, dict)
    assert response == {"message": "Hello, sinsky!"}

def test_describe_method_request(client_tester_reflection_client):
    request_description = \
        client_tester_reflection_client.describe_method_request('client_tester.ClientTester', 'TestUnaryUnary')
    expected_request_description = {
        'factor': 'INT32',
        'readings': 'FLOAT',
        'uuid': 'UINT64',
        'sample_flag': 'BOOL',
        'request_name': 'STRING',
        'extra_data': 'BYTES'
    }
    assert (
        request_description == expected_request_description
    ), f"Expected: {expected_request_description}, Actual: {request_description}"

def test_describe_request(client_tester_reflection_client):
    request_description = \
        client_tester_reflection_client.describe_request('client_tester.ClientTester', 'TestUnaryUnary')
    expected_request_description = """TestRequest
Fields:
\tfactor: INT32
\treadings: FLOAT
\tuuid: UINT64
\tsample_flag: BOOL
\trequest_name: STRING
\textra_data: BYTES"""
    assert request_description == expected_request_description

def test_describe_response(client_tester_reflection_client):
    request_description = \
        client_tester_reflection_client.describe_response('client_tester.ClientTester', 'TestUnaryUnary')
    expected_response_description = """TestResponse
Fields:
\taverage: DOUBLE
\tfeedback: STRING"""
    assert request_description == expected_response_description

def test_empty_body_request(helloworld_reflection_client):
    response = helloworld_reflection_client.request('helloworld.Greeter', 'SayHello', {})
    assert isinstance(response, dict)

def test_nonexistent_service(helloworld_reflection_client):
    with pytest.raises(ValueError):
        helloworld_reflection_client.request('helloworld.Speaker', 'SingHello', {})

def test_nonexistent_method(helloworld_reflection_client):
    with pytest.raises(ValueError):
        helloworld_reflection_client.request('helloworld.Greeter', 'SayGoodbye', {})

def test_unsupported_argument(helloworld_reflection_client):
    with pytest.raises(ParseError):
        helloworld_reflection_client.request('helloworld.Greeter', 'SayHello', {"foo": "bar"})

def test_unary_stream(helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    responses = helloworld_reflection_client.request(
        'helloworld.Greeter',
        'SayHelloGroup',
        {"name": "".join(name_list)}
    )
    assert all(isinstance(response, dict) for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello, {name}!"}

def test_stream_unary(helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    response = helloworld_reflection_client.request(
        'helloworld.Greeter',
        'HelloEveryone',
        [{"name": name} for name in name_list]
    )
    assert isinstance(response, dict)
    assert response == {'message': f'Hello, {" ".join(name_list)}!'}

def test_stream_stream(helloworld_reflection_client):
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    responses = helloworld_reflection_client.request(
        'helloworld.Greeter',
        'SayHelloOneByOne',
        [{"name": name} for name in name_list]
    )
    assert all(isinstance(response, dict) for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello, {name}!"}

def test_reflection_service_client(helloworld_reflection_client):
    svc_client = helloworld_reflection_client.service('helloworld.Greeter')
    method_names = svc_client.method_names
    assert method_names == ('SayHello', 'SayHelloGroup', 'HelloEveryone', 'SayHelloOneByOne')

def test_reflection_service_client_invalid_service(helloworld_reflection_client):
    with pytest.raises(ValueError):
        helloworld_reflection_client.service('helloWorld.Singer')
