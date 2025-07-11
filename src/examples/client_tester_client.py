from grpc_requests.client import Client
from grpc_requests.utils import CredentialsInfo

"""
client_tester_reflection

An example of how grpc_requests works against a reflection enabled grpc server.

In order for this example to work, the example client_tester server must be
running.
"""

host = "localhost"
port = "50052"
endpoint = f"{host}:{port}"
ssl_credentials = CredentialsInfo(root_certificates='~/.local/share/mkcert/rootCA.pem', certificate_chain=None, private_key=None)

print(ssl_credentials)

client = Client.get_by_endpoint(endpoint, credentials=ssl_credentials)

service = "client_tester.ClientTester"

# Unary-Unary Example

unary_unary_method = "TestUnaryUnary"
unary_unary_request = {}

response = client.unary_unary(service, unary_unary_method, unary_unary_request)
print(response)

# Unary-Stream Example

# unary_stream_method = "TestUnaryStream"
# unary_stream_request = {}

# responses = client.unary_stream(service, unary_stream_method, unary_stream_request)
# print(responses)

# # Stream-Unary Example

# stream_unary_method = "TestStreamUnary"
# stream_unary_request = [{}, {}, {}]

# response = client.stream_unary(service, stream_unary_method, stream_unary_request)
# print(response)

# # Stream-Stream Example

# stream_stream_method = "TestStreamStream"
# stream_stream_request = [{}, {}, {}]

# responses = client.stream_stream(service, stream_stream_method, stream_stream_request)
# print(responses)

exit()
