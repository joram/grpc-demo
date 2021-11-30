setup:
	pip install grpcio-tools Faker

generate_definitions:
	mkdir ./generated
	touch ./generated/__init__.py
	python3 -m grpc_tools.protoc --python_out=./generated --grpc_python_out=./generated -I./protos demo.proto

run_server:
	PYTHONPATH=./generated/ python3 ./server.py

run_client:
	PYTHONPATH=./generated/ python3 ./client.py 1

run_client_1000:
	PYTHONPATH=./generated/ python3 ./client.py 1000