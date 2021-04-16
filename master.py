from redis import Redis
from rq import Queue
import grpc
from concurrent import futures      #with master this goes out
import proto.task_pb2_grpc as pb2_grpc
import proto.task_pb2 as pb2

import time

from tasks import *

TASKS = {
    'countingWords': countingWords,
    'wordCount': wordCount
}

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

r = Redis(host=REDIS_HOST, port=REDIS_PORT)
q = Queue(connection=r)

class TaskService(pb2_grpc.SendTaskServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):
        taskName = request.task
        fileName = request.file

        #print("Task name: "+TaskName)
        #print("File name: "+FileName)
        if taskName not in TASKS:
            return pb2.TaskResponse(**{'result': "Task does not exist"})

        job = q.enqueue(TASKS[taskName], fileName, result_ttl=100)
        print(f"JOB ID: {job.get_id()}")

        while not job.is_finished:
            time.sleep(0.1)
            print("Not finished")
        return pb2.TaskResponse(**{'result': str(job.result)})

def serve():
    print("Initialized! We are ready")
    print("Waiting for client...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SendTaskServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Make sure http.server is active")
    print("Initializing server...")
    serve()

