from redis import Redis
from rq import Queue

import time

from tasks import *

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

r = Redis(host=REDIS_HOST, port=REDIS_PORT)
q = Queue(connection=r)

r.flushall

t0 = time.time()
jobs = []


for _ in range(10):
 jobs.append(q.enqueue(wordCount, 'test_word_count.txt', result_ttl=-1))
 jobs.append(q.enqueue(countingWords, 'test_word_count.txt', result_ttl=-1))

#time.sleep(5)
while any(not job.is_finished for job in jobs):
	time.sleep(1)

for job in jobs:
	print(job.result)

t1 = time.time()
print(t1 - t0)
