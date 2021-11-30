import time
import uuid
from concurrent import futures

import grpc

from generated.demo_pb2 import BackgroundCheckRequest, BackgroundCheckResponse
from generated.demo_pb2_grpc import BackgroundCheckServiceServicer, add_BackgroundCheckServiceServicer_to_server
from validation import RequestHeaderValidatorInterceptor


class BackgroundCheckServicer(BackgroundCheckServiceServicer):
    calls = 0

    def CreateBackgroundCheck(self, request: BackgroundCheckRequest, context: grpc.ServicerContext):
        print(request)
        return BackgroundCheckResponse(id=f"backgroundcheck_{str(uuid.uuid4()).replace('-', '')}")


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[RequestHeaderValidatorInterceptor("x-api-key", "fake_api_key", 403, "not allowed")],
    )
    add_BackgroundCheckServiceServicer_to_server(BackgroundCheckServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


serve()
