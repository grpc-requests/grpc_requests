import pytest

from grpc_requests.utils import CredentialsInfo, load_data

ROOT_CERT_PATH = "./src/tests/test_servers/credentials/localhost.pem"
PRIVATE_KEY_PATH = "./src/tests/test_servers/credentials/localhost-key.pem"

@pytest.mark.parametrize(
    "root_certificate, private_key, certificate_chain",
    [
        # Path-based values
        (ROOT_CERT_PATH, PRIVATE_KEY_PATH, None),
        (ROOT_CERT_PATH, load_data(PRIVATE_KEY_PATH), None),
        (ROOT_CERT_PATH, None, None),
        (load_data(ROOT_CERT_PATH), PRIVATE_KEY_PATH, None),
        (load_data(ROOT_CERT_PATH), load_data(PRIVATE_KEY_PATH), None),
        (load_data(ROOT_CERT_PATH), None, None),
        (None, PRIVATE_KEY_PATH, None),
        (None, load_data(PRIVATE_KEY_PATH), None),
        (None, None, None),
    ],
)
def test_credential_info(root_certificate, private_key, certificate_chain):
    credentials = CredentialsInfo(root_certificates=root_certificate, private_key=private_key, certificate_chain=certificate_chain)
    assert credentials is not None
