from multiprocessing import Process, cpu_count
from redis import Redis
from rq import Worker

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

WORKERS = {}
WORKERS_ID = 0

def processTask():
	r = Redis(host=REDIS_HOST, port=REDIS_PORT)
	w = Worker(['default'], connection=r)
	w.work()


def createWorker():
    global WORKERS
    global WORKERS_ID

    proc = Process(target=processTask, args=())
    proc.start()
    WORKERS[WORKERS_ID] = proc
    WORKERS_ID += 1

    return True

def removeWorker(id):
    if id in WORKERS:
        WORKERS[id].terminate()
        WORKERS.pop(id)
    
    return True

def listWorkers():
    print(WORKERS)

    return True


if __name__ == '__main__':
    createWorker()      #create on worker at least





"""if __name__ == '__main__':
    n = cpu_count()
    print(n)
    ps = []
    for _ in range(n):
        p = Process(target=processTask, args=())
        p.start()
        ps.append(p)        #Perque crear una llista i fer despres join a no fer-ho ja quan fem start
    print(ps)
    for p in ps:
        p.join()"""
