# Examples

A [reflection example](./helloworld_reflection.py) is provided for those wishing to get started quickly.
A [toy server example](./helloworld_server.py) is also provided for additional insight into how the library works.

We also recommend reviewing the unit tests to get an idea of how specific functionality
can be implemented.

- [reflection client tests](../tests/reflection_client_test.py)
- [service client tests](../tests/service_client_test.py)
- [stub client tests](../tests/stub_client_test.py)
- [async client tests](../tests/async_reflection_client_test.py)

In addition, here are some simple examples of utilizing the grpc_requests library
in particular scenarios.

## Connecting to a server requiring authentication

If connecting to a server requiring bearer authentication, that can be provided
as a metadata argument to the `get_by_endpoint` Client method.

This will work similarly for providing other such metadata, such as a Cookie
header.

```python
from grpc_requests import Client

metadata = [("authorization", f"bearer {my_bearer_token}")]
client = Client.get_by_endpoint("my.supercool.hostname:443", ssl=True, metadata=metadata)

health_response = client.request('grpc.health.v1.Health', 'Check', {}, metadata=metadata)

assert health_response == {"status": "SERVING"}
```

## Making requests using reflection

If connecting to a server that is generally unknown, but does implement
reflection, you can enumerate the services and methods of that server and
pass request bodies directly as Dictionaries to explore the server.

```python
from grpc_requests import Client

client = Client.get_by_endpoint("localhost:50051")

assert client.service_names == ["helloworld.Greeter",  "grpc.health.v1.Health"]

assert client.service.method_names == ["SayHello", "SayHelloGroup", "HelloEveryone", "SayHelloOneByOne"]

say_hello_response = client.request("helloworld.Greeter","SayHello",{"name": "sinsky"})
assert say_hello_response == {"message", "Hello Sinsky!"}
```

## Making requests with a reflected stub client

If the server being connected to supports reflection, it is also possible to
create a stub client for a specific service.

```python
from grpc_requests import Client
from helloworld_pb2 import HelloRequest

client = Client.get_by_endpoint("localhost:50051")
assert client.service_names == ["helloworld.Greeter",  "grpc.health.v1.Health"]

greeter = client.service("helloworld.Greeter")

names = ["sinsky", "viridianforge"]
requests_data = [{"name": name} for name in name_list]
hello_everyone_response = greeter.HelloEveryone(requests_data)
assert hello_everyone_response == {'message': f'Hello, {" ".join(name_list)}!'}
```

## Making requests using a stub instantiated client

If the server being connected to does not support reflection, but makes their
protobuf stubs available, they can be leveraged to facilitate interacton.

```python
from grpc_requests import StubClient
from .helloworld_pb2 import Descriptor

service_descriptor = DESCRIPTOR.services_by_name['Greeter'] # or you can just use _GREETER

client = StubClient.get_by_endpoint("localhost:50051", service_descriptors=[service_descriptor,])
assert client.service_names == ["helloworld.Greeter"]

greeter = client.service("helloworld.Greeter")

names = ["sinsky", "viridianforge"]
requests_data = [{"name": name} for name in name_list]
results = greeter.SayHelloOneByOne(requests_data)
for response, name in zip(responses, name_list):
    assert response == {"message": f"Hello, {name}!"}
```

## Asynchronously making requests to a server

An async client is provided that can be used with standard async Python libraries
to facilitate asynchronous interactions with grpc servers.

```python
from grpc_requests.aio import AsyncClient

client = AsyncClient("localhost:50051")

health = await client.service("grpc.health.v1.Health")
assert health.method_names == ("Check", "Watch")

result = await health.Check()
assert result == {"status": "SERVING"}

greeter = await client.service("helloworld.Greeter")

request_data = {"name": "sinsky"}
result = await greeter.SayHello(request_data)

results =[x async for x in await greeter.SayHelloGroup(request_data)] 

requests_data = [{"name": "sinsky"}]
result = await greeter.HelloEveryone(requests_data)
results = [x async for x in await greeter.SayHelloOneByOne(requests_data)]  
```

## Retrieving Information about a Server

All forms of clients expose methods to allow a user to query a server about its
provided services and their methods.

Examples are provided using the Client type, but the same methods are on the
AsyncClient as well.

### Retrieving Descriptors from a Server

```python
from grpc_requests.client import Client

client = Client("localhost:50051")

greeterServiceDescriptor = client.get_service_descriptor("helloworld.Greeter")
sayHelloDescriptor = client.get_method_descriptor("helloworld.Greeter","SayHello")

#As of 0.1.14 FileDescriptor Methods are only exposed on Reflection Clients
fileDescriptorByName = client.get_file_descriptor_by_name("helloworld.proto")
fileDescriptorBySymbol = client.get_file_descriptor_by_symbol("helloworld.Greeter")
```

### Method Metadata

grpc_requests utilizes MethodMetaData objects to organize the methods of the
services of the servers clients are built for.

```python
from grpc_requests.client import Client

client = Client("localhost:50051")

sayHelloMethodMetaData = client.get_method_meta("helloworld.Greeter", "SayHello")

sayHelloInputType = sayHelloMethodMetaData.input_type
sayHelloOutputType = sayHelloMethodMetaData.output_type
sayHelloDescriptor = sayHelloMethodMetaData.descriptor

assert sayHelloDescriptor.name == "SayHello"
assert sayHelloDescriptor.containing_service.name == "helloworld.Greeter"
```

### Describing Requests and Responses

grpc_requests makes available two experimental methods to provide users ways
to retrieve human readable descriptions of the request and response for implementer
review.

```python
from grpc_requests.client import Client

client = Client("localhost:50051")

sayHelloRequestDescription = client.describe_request("helloworld.Greeter", "SayHello")
sayHelloResponseDescription = client.describe_response("helloworld.Greeter", "SayHello")

print(sayHelloRequestDescription)
print(sayHelloResponseDescription)
```
