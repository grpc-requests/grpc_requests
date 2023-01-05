# grpc requests

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/grpc-requests?style=flat-square)](https://pypi.org/project/grpc-requests)
[![PyPI](https://img.shields.io/pypi/v/grpc-requests?style=flat-square)](https://pypi.org/project/grpc-requests)
[![PyPI download month](https://img.shields.io/pypi/dm/grpc-requests?style=flat-square)](https://pypi.org/project/grpc-requests)
[![codecov](https://codecov.io/gh/spaceone-dev/grpc_requests/branch/master/graph/badge.svg)](https://codecov.io/gh/spaceone-dev/grpc_requests)
![Views](https://views.whatilearened.today/views/github/spaceone-dev/grpc_requests.svg)

## GRPC for Humans

```python
from grpc_requests import Client

client = Client.get_by_endpoint("localhost:50051")
assert client.service_names == ["helloworld.Greeter"]

request_data = {"name": 'sinsky'} 
result = client.request("helloworld.Greeter", "SayHello", request_data)
print(result) # {"message":"Hellow sinsky"}

```

## Features

- supports creating clients easily when connecting to servers implementing grpc reflection
- supports implementing stub clients for connecting to servers that do not implement reflection
- support all unary and stream methods
- supports both TLS and compression connections
- supports AsyncIO API

## Install

```shell script
pip install grpc_requests
```

## Use it like RPC

If your server supports reflection, use the `Client` class:

```python
from grpc_requests import Client

client = Client.get_by_endpoint("localhost:50051")
# if you want a TLS connection
# client = Client.get_by_endpoint("localhost:443",ssl=True)
# or if you want a compression enabled connection
# client = Client.get_by_endpoint("localhost:443",compression=grpc.Compression.Gzip)
assert client.service_names == ["helloworld.Greeter",'grpc.health.v1.Health']

health = client.service('grpc.health.v1.Health')
assert health.method_names == ('Check', 'Watch')

result = health.Check()
assert result == {'status': 'SERVING'}
```

If not, use the `StubClient` class:

```python
from grpc_requests import StubClient
from .helloworld_pb2 import Descriptor

service_descriptor = DESCRIPTOR.services_by_name['Greeter'] # or you can just use _GREETER


client = StubClient.get_by_endpoint("localhost:50051",service_descriptors=[service_descriptor,])
assert client.service_names == ["helloworld.Greeter"]
```

In both cases, the same methods are used to interact with the server.

```python
greeter = client.service("helloworld.Greeter")

request_data = {"name": 'sinsky'}
result = greeter.SayHello(request_data)
results = greeter.SayHelloGroup(request_data)

requests_data = [{"name": 'sinsky'}]
result = greeter.HelloEveryone(requests_data)
results = greeter.SayHelloOneByOne(requests_data)

```

## Examples

- [helloworld reflection client](src/examples/helloworld_reflection.py)

### Reflection Client but you can send message by stub

```python
from grpc_requests import Client
from helloworld_pb2 import HelloRequest

port = '50051'
host = "localhost"
endpoint = f"{host}:{port}"

client = Client.get_by_endpoint(endpoint)
print(client.service_names) # ["helloworld.Greeter"]

service = "helloworld.Greeter"
method = 'SayHello'

result = client.unary_unary(service, method, HelloRequest(name='sinsky'))
print(type(result)) # result is dict Type!!! not Stub Object!
print(result) # {"message":"Hellow sinsky"}

# or get raw response data
result = client.unary_unary(service, method, HelloRequest(name='sinsky'),raw_output=True)
print(type(result)) # HelloReply stub class
```

### AsyncIO API

```python
from grpc_requests.aio import AsyncClient

client = AsyncClient("localhost:50051")

health = await client.service('grpc.health.v1.Health')
assert health.method_names == ('Check', 'Watch')

result = await health.Check()
assert result == {'status': 'SERVING'}

greeter = await client.service("helloworld.Greeter")

request_data = {"name": 'sinsky'}
result = await greeter.SayHello(request_data)

results =[x async for x in await greeter.SayHelloGroup(request_data)] 

requests_data = [{"name": 'sinsky'}]
result = await greeter.HelloEveryone(requests_data)
results = [x async for x in await greeter.SayHelloOneByOne(requests_data)]  

```

## Road map

- [x] support no reflection server(Stub Client)
- [x] support async API!
- [ ] Document!
- [ ] pluggable interceptor

## Maintainers

- sinsky - [wesky93](https://github.com/wesky93)
- Wayne Manselle - [ViridianForge](https://github.com/ViridianForge)
