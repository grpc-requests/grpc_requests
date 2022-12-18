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

- connect server using reflection or Stub
- no need stub class request grpc(if you want)
- support all unary &  stream method
- support tls & compression connect
- support AsyncIO API

## Install

```shell script
pip install grpc_requests
```

## Use it like RPC

If your server supports reflection:

```python
from grpc_requests import Client

client = Client.get_by_endpoint("localhost:50051")
# if you want connect tls
# client = Client.get_by_endpoint("localhost:443",ssl=True)
# or if you want Compression connect
# client = Client.get_by_endpoint("localhost:443",compression=grpc.Compression.Gzip)
assert client.service_names == ["helloworld.Greeter",'grpc.health.v1.Health']

health = client.service('grpc.health.v1.Health')
assert health.method_names == ('Check', 'Watch')

result = health.Check()
assert result == {'status': 'SERVING'}

greeter = client.service("helloworld.Greeter")

request_data = {"name": 'sinsky'}
result = greeter.SayHello(request_data)
results = greeter.SayHelloGroup(request_data)

requests_data = [{"name": 'sinsky'}]
result = greeter.HelloEveryone(requests_data)
results = greeter.SayHelloOneByOne(requests_data)

```

If not you can also use your stub client:

```python
from grpc_requests import StubClient
from .hellow_pb2 import Descriptor

service_descriptor = DESCRIPTOR.services_by_name['Greeter'] # or you can just use _GREETER


client = StubClient.get_by_endpoint("localhost:50051",service_descriptors=[service_descriptor,])
# if you want connect tls
# client = Client.get_by_endpoint("localhost:443",ssl=True)
# or if you want Compression connect
# client = Client.get_by_endpoint("localhost:443",compression=grpc.Compression.Gzip)
assert client.service_names == ["helloworld.Greeter"]
greeter = client.service("helloworld.Greeter")

request_data = {"name": 'sinsky'}
result = greeter.SayHello(request_data)
results = greeter.SayHelloGroup(request_data)

requests_data = [{"name": 'sinsky'}]
result = greeter.HelloEveryone(requests_data)
results = greeter.SayHelloOneByOne(requests_data)

```

## Examples

### Request unary-unary

```python
service = "helloworld.Greeter"
unary_unary_method = 'SayHello'

request_data = {"name": 'sinsky'} # You Don't Need Stub!
result = client.request(service, unary_unary_method, request_data)
assert dict == type(result) # result is dict Type!!! not Stub Object!
assert {"message":"Hellow sinsky"} == result

# or

request_data = {"name": 'sinsky'} # You Don't Need Stub!
# any one know this method is unary-unary
result = client.unary_unary(service, unary_unary_method, request_data) 
assert dict == type(result) # result is dict Type!!! not Stub Object!
assert {"message":"Hellow sinsky"} == result
```

### Request unary-stream

```python
unary_stream_method = 'SayHelloGroup'
unary_stream_results = client.request(service, unary_unary_method, request_data)
assert all([dict == type(result) for result in unary_stream_results])
assert [{"message":"Hellow sinsky"}] == list(unary_stream_results)

# or

unary_stream_results = client.unary_stream(service, unary_unary_method, request_data)
assert all([dict == type(result) for result in unary_stream_results])
assert [{"message":"Hellow sinsky"}] == list(unary_stream_results)
```

### Request stream-unary

```python
requests_data = [request_data] # iterator
stream_unary_method = 'HelloEveryone'

result_stream_unary = client.request(service, stream_unary_method, requests_data)
assert dict == type(result) # result is dict Type!!! not Stub Object!

# or

result_stream_unary = client.stream_unary(service, stream_unary_method, requests_data)
assert dict == type(result) # result is dict Type!!! not Stub Object!
```

### Request stream-stream

```python
requests_data = [request_data] # iterator
stream_stream_method = 'SayHelloOneByOne'

result = client.request(service, stream_stream_method,requests_data )
assert all([dict == type(result) for result in unary_stream_results])

# or

result = client.stream_stream(service, stream_stream_method,requests_data )
assert all([dict == type(result) for result in unary_stream_results])
```

##  Reflection Client but you can send mesg by stub

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

## AsyncIO API

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
- [ ] plugable interceptor

## Change Logs

- [0.1.7](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.1.7)
  - remove homi & test code
- [0.1.6](https://github.com/spaceone-dev/grpc_requests/releases/tag/v0.1.6)
- 0.1.3
  - :bug:
    - remove click
  - :warning:
    - ignore test before deploy...
- 0.1.1
    - Change
        - remove unused package : click #35
- 0.1.0
    - :sparkles: Feature
        - #29 support fully TLS connect
    - :bug:
        - #30 ignore reflection if already registered service
    - Change
      - #23 grpcio version up 
- 0.0.10
    - :bug:
        - #19 fix 3.6 compatibility issue : await is in f-string
- 0.0.9 
    - :sparkles: Feature
        - #13 support AsyncIO API
- 0.0.8
    - :sparkles: Feature
        - #12 add StubClient
    - :bug: Bug Fix!
        - #11 bypasss kwargs to base client
- 0.0.7
    - Feature
        - support Compression
        
- 0.0.6
    - Feature
        - support tls connect      

- 0.0.5
    - Change
        - response filed get orginal proto field(before returend lowerCamelCase)  

- 0.0.3
    - Feature
        - dynamic request method
        - service client

- 0.0.2
    - support all method type
    - add request test case

- 0.0.1
    - sync proto using reflection
    - auto convert request(response) from(to) dict
    - support unary-unary
