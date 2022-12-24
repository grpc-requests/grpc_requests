from grpc_requests.client import Client

"""
helloworld_reflection

An example of how grpc_requests works against a reflection enabled grpc server.

In order for this example to work, the example helloworld server must be
running.
"""

host = 'localhost'
port = '50051'
endpoint = f"{host}:{port}"

client = Client.get_by_endpoint(endpoint)

service = 'helloworld.Greeter'
name_list = ["sinsky", "viridianforge", "jack", "harry"]
name_string = " ".join(name_list)

# Unary-Unary Example

unary_unary_method = 'SayHello'
unary_unary_request = {"name": "sinsky"}

response = client.unary_unary(service, unary_unary_method, unary_unary_request)
assert type(response) == dict
assert response == {"message": "Hello, sinsky!"}

# Unary-Stream Example

unary_stream_method = 'SayHelloGroup'
unary_stream_request = {"name": "".join(name_list)}

responses = client.unary_stream(service, unary_stream_method, unary_stream_request)
assert all(type(response) == dict for response in responses)
for response, name in zip(responses, name_list):
  assert response == {"message": f"Hello, {name}!"}

# Stream-Unary Example

stream_unary_method = 'HelloEveryone'
stream_unary_request = [{"name": name} for name in name_list]

response = client.stream_unary(service, stream_unary_method, stream_unary_request)
assert type(response) == dict
assert response == {'message': f"Hello, {name_string}!"}

# Stream-Stream Example

stream_stream_method = 'SayHelloOneByOne'
stream_stream_request = [{"name": name} for name in name_list]

responses = client.stream_stream(service, stream_stream_method, stream_stream_request)
assert all(type(response) == dict for response in responses)
for response, name in zip(responses, name_list):
  assert response == {"message": f"Hello, {name}!"}
