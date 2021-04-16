import grpc
from concurrent import futures      #with master this goes out
import proto.task_pb2_grpc as pb2_grpc
import proto.task_pb2 as pb2

class TaskService(pb2_grpc.SendTaskServicer):
    
    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):

        # get the string from the incoming request
        TaskName = request.task
        FileName = request.file
        result = {'result':'10'}
        print(result)

        return pb2.TaskResponse(**result)


def serve():
    print("Initialized! We are ready")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SendTaskServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Initializing server...")
    serve()


