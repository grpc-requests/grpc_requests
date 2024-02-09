import logging
import pytest

from grpc_requests.aio import AsyncClient, MethodType
from google.protobuf.json_format import ParseError
import grpc.aio

from tests.common import AsyncMetadataClientInterceptor
from tests.test_servers.dependencies import (
    dependencies_pb2,
    dependency1_pb2,
    dependency2_pb2,
)
from google.protobuf import descriptor_pool, descriptor_pb2

"""
Test cases for async reflection based client
"""

logger = logging.getLogger("name")


@pytest.mark.asyncio
async def test_unary_unary():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    greeter_service = await client.service("helloworld.Greeter")
    response = await greeter_service.SayHello({"name": "sinsky"})
    assert isinstance(response, dict)
    assert response == {"message": "Hello, sinsky!"}


@pytest.mark.asyncio
async def test_unary_unary_interceptor():
    client = AsyncClient(
        "localhost:50051",
        interceptors=[AsyncMetadataClientInterceptor()],
        descriptor_pool=descriptor_pool.DescriptorPool(),
    )
    greeter_service = await client.service("helloworld.Greeter")
    response = await greeter_service.SayHello({"name": "sinsky"})
    assert isinstance(response, dict)
    assert response == {"message": "Hello, sinsky, interceptor accepted!"}


@pytest.mark.asyncio
async def test_methods_meta():
    client = AsyncClient(
        "localhost:50051",
        interceptors=[AsyncMetadataClientInterceptor()],
        descriptor_pool=descriptor_pool.DescriptorPool(),
    )
    greeter_service = await client.service("helloworld.Greeter")
    meta = greeter_service.methods_meta
    assert meta["HelloEveryone"].method_type == MethodType.STREAM_UNARY


@pytest.mark.asyncio
async def test_empty_body_request():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    greeter_service = await client.service("helloworld.Greeter")
    response = await greeter_service.SayHello({})
    assert isinstance(response, dict)


@pytest.mark.asyncio
async def test_nonexistent_method():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    greeter_service = await client.service("helloworld.Greeter")
    with pytest.raises(AttributeError):
        await greeter_service.SayGoodbye({})


@pytest.mark.asyncio
async def test_unsupported_argument():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    greeter_service = await client.service("helloworld.Greeter")
    with pytest.raises(ParseError):
        await greeter_service.SayHello({"foo": "bar"})


@pytest.mark.asyncio
async def test_unary_stream():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    greeter_service = await client.service("helloworld.Greeter")
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    responses = [
        x
        async for x in await greeter_service.SayHelloGroup(
            [{"name": name} for name in name_list]
        )
    ]
    assert all(isinstance(response, dict) for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello, {name}!"}


@pytest.mark.asyncio
async def test_stream_unary():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    greeter_service = await client.service("helloworld.Greeter")
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    response = await greeter_service.HelloEveryone(
        [{"name": name} for name in name_list]
    )
    assert isinstance(response, dict)
    assert response == {
        "message": f'Hello, {" ".join(["sinsky", "viridianforge", "jack", "harry"])}!'
    }


@pytest.mark.asyncio
async def test_stream_stream():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    greeter_service = await client.service("helloworld.Greeter")
    name_list = ["sinsky", "viridianforge", "jack", "harry"]
    responses = [
        x
        async for x in await greeter_service.SayHelloOneByOne(
            [{"name": name} for name in name_list]
        )
    ]
    assert all(isinstance(response, dict) for response in responses)
    for response, name in zip(responses, name_list):
        assert response == {"message": f"Hello {name}"}


@pytest.mark.asyncio
async def test_reflection_service_client():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    greeter_service = await client.service("helloworld.Greeter")
    method_names = greeter_service.method_names
    assert method_names == (
        "SayHello",
        "SayHelloGroup",
        "HelloEveryone",
        "SayHelloOneByOne",
    )


@pytest.mark.asyncio
async def test_reflection_service_client_invalid_service():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    with pytest.raises(ValueError):
        await client.service("helloWorld.Singer")


@pytest.mark.asyncio
async def test_get_service_descriptor():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    await client.register_service("helloworld.Greeter")
    service_descriptor = client.get_service_descriptor("helloworld.Greeter")
    assert service_descriptor.name == "Greeter"


@pytest.mark.asyncio
async def test_get_file_descriptor_by_name():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    file_descriptors = await client.get_file_descriptors_by_name("helloworld.proto")
    assert file_descriptors[0].name == "helloworld.proto"
    assert file_descriptors[0].package == "helloworld"
    assert file_descriptors[0].syntax == "proto3"


@pytest.mark.asyncio
async def test_get_file_descriptors_by_name():
    client = AsyncClient(
        "localhost:50053", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    file_descriptor = await client.get_file_descriptors_by_name("dependencies.proto")
    assert file_descriptor[0].name == "dependencies.proto"
    assert file_descriptor[1].name == "dependency1.proto"
    assert file_descriptor[2].name == "dependency2.proto"


@pytest.mark.asyncio
async def test_get_file_descriptor_by_symbol():
    client = AsyncClient(
        "localhost:50051", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    file_descriptors = await client.get_file_descriptors_by_symbol("helloworld.Greeter")
    assert file_descriptors[0].name == "helloworld.proto"
    assert file_descriptors[0].package == "helloworld"
    assert file_descriptors[0].syntax == "proto3"


@pytest.mark.asyncio
async def test_get_file_descriptors_by_symbol():
    client = AsyncClient(
        "localhost:50053", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    file_descriptor = await client.get_file_descriptors_by_symbol(
        "dependencies.Greeter"
    )
    assert file_descriptor[0].name == "dependencies.proto"
    assert file_descriptor[1].name == "dependency1.proto"
    assert file_descriptor[2].name == "dependency2.proto"


@pytest.mark.asyncio
async def test_register_file_descriptors_no_lookup():
    # Connect to not a real server to make sure we do local lookup
    client = AsyncClient(
        "localhost:notaport", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    descriptors = [
        dependencies_pb2.DESCRIPTOR,
        dependency1_pb2.DESCRIPTOR,
        dependency2_pb2.DESCRIPTOR,
    ]
    file_descriptors = []
    for descriptor in descriptors:
        proto = descriptor_pb2.FileDescriptorProto()
        descriptor.CopyToProto(proto)
        file_descriptors.append(proto)
    await client.register_file_descriptors(file_descriptors)


@pytest.mark.asyncio
async def test_register_file_descriptors_incomplete_dependencies():
    # Connect to not a real server to make sure we do local lookup
    client = AsyncClient(
        "localhost:notaport", descriptor_pool=descriptor_pool.DescriptorPool()
    )
    descriptors = [
        dependencies_pb2.DESCRIPTOR,
        dependency1_pb2.DESCRIPTOR,
    ]
    file_descriptors = []
    for descriptor in descriptors:
        proto = descriptor_pb2.FileDescriptorProto()
        descriptor.CopyToProto(proto)
        file_descriptors.append(proto)
    with pytest.raises(grpc.aio._call.AioRpcError):
        await client.register_file_descriptors(file_descriptors)
