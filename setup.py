import re

from setuptools import setup

with open("src/grpc_requests/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open("requirements.txt", encoding="utf8") as f:
    requirements = list(f.readlines())

setup(
    name='grpc_requests',
    version=version,
    install_requires=requirements,
)
