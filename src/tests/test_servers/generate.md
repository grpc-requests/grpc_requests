# Generate proto code

## Dependencies server

1. Generate the code

```sh
python -m grpc_tools.protoc -I./dependencies --python_out=./dependencies --pyi_out=./dependencies --grpc_python_out=./dependencies dependencies/dependencies.proto dependencies/dependency1.proto dependencies/dependency2.proto

sed -i '' 's/^\(import.*_pb2\)/from . \1/' dependencies/*.py
```
