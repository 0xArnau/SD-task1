from redis import Redis
from rq import Queue
import grpc
from concurrent import futures      #with master this goes out
import task_pb2_grpc as pb2_grpc
import task_pb2 as pb2

import time

from tasks import *

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

r = Redis(host=REDIS_HOST, port=REDIS_PORT)
q = Queue(connection=r)

class TaskService(pb2_grpc.SendTaskServicer):
    
    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):
        TaskName = request.task
        FileName = request.file

        #print("Task name: "+TaskName)
        #print("File name: "+FileName)

        job = q.enqueue(TaskName, FileName, result_ttl=0)
        print(job.get_id())

        if job.is_queued:
            print("ENQUEUED")
        
        if job.is_started:
            print("STARTED")
        
        #Result es None
        result = {'result': job.result}
        print(result)

        if job.is_finished:
            print("FINISHED")
        
        return pb2.TaskResponse(**result)

def serve():
    print("Initialized! We are ready")
    print("Waiting for client...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SendTaskServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Initializing server...")
    serve()

