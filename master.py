from multiprocessing import Process
import redis
from rq import Queue

r = redis.Redis()
q = Queue(connection=r)

workers = {}
worker_id = 0


def start_worker(worker_id):
    print("Worker id", worker_id)

def create_worker():
    global workers
    global workersrid

    proc = Process(target=start_worker, args=(worker_id,))
    proc.start()
    workers[worker_id] = proc

    worker_id += 1