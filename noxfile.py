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
def tests(session, protobuf):
    session.install("-e",".")
    session.install("-r", "requirements-test.txt")
    session.install(f"protobuf=={protobuf}")
    session.run("pip", "list")
    session.run("pytest")
