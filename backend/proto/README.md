# Proto definitions

Use the following to generate the Python code from the proto file:
Change 'your_file_name_here' to the desired file name

```shell
python -m grpc_tools.protoc -Ibackend/proto --python_out=backend/common/proto --pyi_out=backend/common/proto --grpc_python_out=backend/common/proto --proto_path=backend/proto/chat.proto backend/proto/your_file_name_here.proto 
```