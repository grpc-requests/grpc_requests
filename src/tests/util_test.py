import pytest

from grpc_requests.utils import CredentialsInfo, load_data


@pytest.fixture(autouse=True)
def generate_tmp_files(tmp_path):
    root_cert_path = tmp_path.joinpath("root_cert.pem")
    private_key_path = tmp_path.joinpath("private_key.pem")
    cert_chain_path = tmp_path.joinpath("cert_chain.pem")

    root_cert_path.write_text("root certificate data")
    private_key_path.write_text("private key data")
    cert_chain_path.write_text("cert chain data")
    yield
    root_cert_path.unlink()
    private_key_path.unlink()
    cert_chain_path.unlink()


@pytest.mark.parametrize(
    ("root_certificate", "private_key", "certificate_chain"),
    [
        (b"mock_root_cert", b"mock_priv_key", b"mock_cert_chain"),
        (b"mock_root_cert", b"mock_priv_key", None),
        (b"mock_root_cert", None, None),
        (None, b"mock_priv_key", None),
        (None, b"mock_priv_key", b"mock_cert_chain"),
        (b"mock_root_cert", None, b"mock_cert_chain"),
        (None, None, None),
    ],
)
def test_credentials_by_bytes(root_certificate, private_key, certificate_chain):
    credentials = CredentialsInfo(
        root_certificates=root_certificate,
        private_key=private_key,
        certificate_chain=certificate_chain,
    )

    assert credentials.root_certificates == root_certificate
    assert credentials.private_key == private_key
    assert credentials.certificate_chain == certificate_chain


@pytest.mark.parametrize(
    ("root_certificate", "private_key", "certificate_chain"),
    [
        ("root_cert.pem", "private_key.pem", "cert_chain.pem"),
        ("root_cert.pem", "private_key.pem", None),
        ("root_cert.pem", None, None),
        (None, "private_key.pem", None),
        (None, "private_key.pem", "cert_chain.pem"),
        ("root_cert.pem", None, "cert_chain.pem"),
        (None, None, None),
    ],
)
def test_credentials_by_files(
    tmp_path, root_certificate, private_key, certificate_chain
):
    expected_rc = None
    expected_pk = None
    expected_cc = None

    if isinstance(root_certificate, str):
        root_certificate = str(tmp_path.joinpath(root_certificate))
        expected_rc = load_data(root_certificate)

    if isinstance(private_key, str):
        private_key = str(tmp_path.joinpath(private_key))
        expected_pk = load_data(private_key)

    if isinstance(certificate_chain, str):
        certificate_chain = str(tmp_path.joinpath(certificate_chain))
        expected_cc = load_data(certificate_chain)

    credentials = CredentialsInfo(
        root_certificates=root_certificate,
        private_key=private_key,
        certificate_chain=certificate_chain,
    )

    assert credentials.root_certificates == expected_rc
    assert credentials.private_key == expected_pk
    assert credentials.certificate_chain == expected_cc
