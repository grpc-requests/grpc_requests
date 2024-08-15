import nox

@nox.session
@nox.parametrize(
    "python,protobuf",
    [
        (python, protobuf)
        for python in ["3.8","3.9","3.10","3.11","3.12"]
        for protobuf in ["4.25.4","5.27.3"]
    ]
)
def test(session, protobuf):
    session.install("-e",".")
    session.install("-r", "requirements-test.txt")
    session.install(f"protobuf=={protobuf}")
    session.run("pytest")

@nox.session
def lint(session):
    session.install("-r", "requirements-lint.txt")
    session.run("ruff", "check", "src/", "--statistics", "--config", "ruff.toml")
    session.run("ruff", "format", "src/", "--config", "ruff.toml")
    session.run("mypy", "src/grpc_requests/")
