import nox


@nox.session
@nox.parametrize(
    "python,protobuf",
    [
        (python, protobuf)
        for python in ["3.9","3.10","3.11","3.12","3.13"]
        for protobuf in ["5.29.5","6.30.2", "6.31.1"]
    ]
)
def test(session, protobuf):
    session.install("-e",".")
    session.install("-r", "requirements-test.txt")
    # Notes!
    session.install(f"protobuf=={protobuf}")
    grpcio = "1.71.0"
    if protobuf == "6.30.2":
        grpcio = "1.72.1"
    if protobuf == "6.31.1":
        grpcio = "1.73.1"
    session.install(f"grpcio=={grpcio}")
    session.install(f"grpcio-reflection=={grpcio}")
    session.run("pytest")

@nox.session
def lint(session):
    session.install("-r", "requirements-lint.txt")
    session.run("ruff", "check", "src/", "--statistics", "--config", "ruff.toml")
    session.run("ruff", "format", "src/", "--config", "ruff.toml")
    session.run("mypy", "src/grpc_requests/")
