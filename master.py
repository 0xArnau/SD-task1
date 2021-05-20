import time
import grpc

from redis import Redis
from rq import Queue, Worker
from multiprocessing import Process, cpu_count
from concurrent import futures      #with master this goes out

import proto.task_pb2_grpc as pb2_grpc
import proto.task_pb2 as pb2

from tasks import *

###################
###    TASKS    ###
###################

TASKS = {
    'countingWords': countingWords,
    'wordCount': wordCount
}

####################
###    WORKER    ###
####################

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

WORKERS = {}
WORKERS_ID = 0

r = Redis(host=REDIS_HOST, port=REDIS_PORT)
q = Queue(connection=r)

def processTask():
	w = Worker(['default'], connection=r)
	w.work()

def createWorker():
    global WORKERS
    global WORKERS_ID

    proc = Process(target=processTask, args=())
    WORKERS[WORKERS_ID] = proc
    WORKERS_ID += 1
    listWorkers()
    proc.start()
    return WORKERS_ID - 1

def removeWorker(id):
    if id in WORKERS:
        WORKERS[id].terminate()
        WORKERS.pop(id)
    
    return True

def listWorkers():
    return WORKERS

def numberWorkers():
    return len(WORKERS)

MANAGE = {
    'createWorker': 'createWorker',
    'removeWorker': 'removeWorker',
    'listWorkers': 'listWorkers',
    'numberWorkers': 'numberWorkers'
}

####################
###    SERVER    ###
####################

class TaskService(pb2_grpc.SendTaskServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):
        taskName = request.task
        arg = request.arg
        
        if taskName in MANAGE:
            if MANAGE[taskName] == 'removeWorker':                          #arg = worker id
                print('Remove Worker')
                result = removeWorker(arg)
                return pb2.TaskResponse(**{'result': str(result)})

            elif MANAGE[taskName] == 'createWorker':
                print('Create Worker')
                result = createWorker()
                return pb2.TaskResponse(**{'result': str(result)})

            elif MANAGE[taskName] == 'numberWorkers':
                print('Number of Workers')
                result = numberWorkers()
                return pb2.TaskResponse(**{'result': str(result)})

            else:                                                           #listWorkers
                print('List Workers')
                result = listWorkers()
                return pb2.TaskResponse(**{'result': str(result)})

        elif taskName in TASKS:
            job = q.enqueue(TASKS[taskName], arg, result_ttl=100)           #arg = URL
            print(f"JOB ID: {job.get_id()}")

            while not job.is_finished:
                time.sleep(.1)
               
            return pb2.TaskResponse(**{'result': str(job.result)})

        else:
            return pb2.TaskResponse(**{'result': "Task does not exist"})    #countingWords, wordCount
  
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

