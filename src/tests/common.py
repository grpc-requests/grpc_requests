import grpc
from grpc_interceptor import ClientCallDetails


class MetadataClientInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, token: str):
        self.token = token

    def intercept_unary_unary(
        self,
        continuation,
        client_call_details,
        request,
    ):
        new_details = ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            [("password", f"{self.token}")],
            client_call_details.credentials,
            client_call_details.wait_for_ready,
            client_call_details.compression,
        )

        return continuation(new_details, request)


class AsyncMetadataClientInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def __init__(self, token: str):
        self.token = token

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        new_details = grpc.aio.ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            [("password", f"{self.token}")],
            client_call_details.credentials,
            client_call_details.wait_for_ready,
        )

        return await continuation(new_details, request)
