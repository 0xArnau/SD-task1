from multiprocessing import Process, cpu_count
from redis import Redis
from rq import Worker

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

def processTask():
	r = Redis(host=REDIS_HOST, port=REDIS_PORT)
	w = Worker(['default'], connection=r)
	w.work()
   


if __name__ == '__main__':
    n = cpu_count()
    ps = []
    for _ in range(n):
        p = Process(target=processTask, args=())
        p.start()
        ps.append(p)
    for p in ps:
        p.join()