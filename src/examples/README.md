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

## Setting a Client's message_to_dict behavior

By utilizing `CustomArgumentParsers`, behavioral arguments can be passed to
message_to_dict at time of Client instantiation. This is available for both
synchronous and asynchronous clients.

```python
client = Client(
            "localhost:50051",
            message_parsers=CustomArgumentParsers(
                message_to_dict_kwargs={
                    "preserving_proto_field_name": True,
                    "including_default_value_fields": True,
                }
            ),
        )
```

[Review the json_format documentation for what kwargs are available to message_to_dict.](https://googleapis.dev/python/protobuf/latest/google/protobuf/json_format.html)

## Creating an async lazy client
An async lazy client can be used to improve startup performance, because the client doesn't need to perform some actions (like service discovery and method registration) during initialization.
You can choose whether to use a lazy client or a non-lazy client based on your program's specific requirements. If you're sure that you'll need to use all of the client's operations as soon as the client is created, then a non-lazy (eager) client might be more suitable. If you only need to use certain operations and you're not sure when you'll need to use them, then a lazy client might be a better choice.
```python
from grpc_requests.aio import AsyncClient

client_lazy = AsyncClient("localhost:50051", lazy=True)
await client_lazy.get_methods_meta("helloworld.Greeter")
print(f"INFO: registered service methods length for lazy client: {len(client_lazy._service_methods_meta)}")

client_nonlazy = AsyncClient("localhost:50051", lazy=False)
await client_nonlazy.get_methods_meta("helloworld.Greeter")
print(f"INFO: registered service methods length for non-lazy client: {len(client_nonlazy._service_methods_meta)}")
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

# As of 0.1.14 FileDescriptor Methods are only exposed on Reflection Clients
# As of 0.1.15 all descriptors related to the name or symbol will be returned as a list
helloworldFileDescriptors = client.get_file_descriptors_by_name("helloworld.proto")
greeterServiceFileDescriptors = client.get_file_descriptors_by_symbol("helloworld.Greeter")
```

### Registering Descriptors Directly

In the event a message is utilized by a service, but not directly referenced
by the typing in the reflected service (i.e. a specific type of metadata served
by a service implementing a [longrunning operation](https://google.aip.dev/151)), that message can
be added directly as follows:

```python
from grpc_requests.client import Client

from grpc_requests.client import Client

client = Client("localhost:50051")

hiddenMessageFileDescriptors = client.get_file_descriptors_by_name("hiddenMessage.proto")
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
