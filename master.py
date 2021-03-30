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
        jobs = []
        TaskName = request.task
        FileName = request.file

        #els workers peten per aqui

        jobs.append(q.enqueue(TaskName, FileName, result_ttl=-1))

        while any(not job.is_finished for job in jobs):
            time.sleep(1)
        
        for job in jobs:
	        print(job.result)
        
        result = {'result': jobs[0].result}
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

