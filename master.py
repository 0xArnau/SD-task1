from redis import Redis
from rq import Queue
import grpc
from concurrent import futures      #with master this goes out
import proto.task_pb2_grpc as pb2_grpc
import proto.task_pb2 as pb2

import time

from worker import createWorker, removeWorker, listWorkers
from tasks import *

TASKS = {
    'countingWords': countingWords,
    'wordCount': wordCount
}

MANAGE = {
    'createWorker': createWorker,
    'removeWorker': removeWorker,
    'listWorkers': listWorkers
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
        arg = request.arg
            
        if taskName in MANAGE:
            if MANAGE[taskName] == 'removeWorker':
                job = q.enqueue(MANAGE[taskName], arg, result_ttl=100)      #arg = worker id or -1 for removing a random one
            else:
                job = q.enqueue(MANAGE[taskName], result_ttl=100)           #createWorker, listWorkers
        elif taskName in TASKS:
            job = q.enqueue(TASKS[taskName], arg, result_ttl=100)           #arg = URL
        else:
            return pb2.TaskResponse(**{'result': "Task does not exist"})    #countingWords, wordCount
        
        print(f"JOB ID: {job.get_id()}")

        while not job.is_finished:
            time.sleep(2)
            print("Not finished")
        return pb2.TaskResponse(**{'result': str(job.result)})

def serve():
    print("Initialized! We are ready")
    print("Waiting for client...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SendTaskServicer_to_server(TaskService(), server)
    #pb2_grpc.add_ManageWorkersServicer_to_server(WorkManage(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Make sure http.server is active")
    print("Initializing server...")
    serve()

