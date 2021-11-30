import sys

import grpc
from faker import Faker

from generated.demo_pb2 import BackgroundCheckRequest, Name
from generated.demo_pb2_grpc import BackgroundCheckServiceStub


def create_background_check(num_calls: int):
    fake = Faker()
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = BackgroundCheckServiceStub(channel)
        request = BackgroundCheckRequest(
            name=Name(
                first_name=fake.first_name(),
                middle_name=fake.last_name(),
                last_name=fake.last_name(),
            ),
            checks=[
                BackgroundCheckRequest.CheckOptions.ONEID,
                BackgroundCheckRequest.CheckOptions.RCMP,
            ]
        )

        for i in range(0, num_calls):
            try:
                response = stub.CreateBackgroundCheck(
                    request,
                    timeout=0.01,
                    metadata=[('x-api-key', "fake_api_key")],
                )
                print(f"created a background check with id {response.id}")
            except Exception as e:
                print(e)



if __name__ == "__main__":
    create_background_check(int(sys.argv[1]))
