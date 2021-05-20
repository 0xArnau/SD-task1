import grpc
import proto.task_pb2_grpc as pb2_grpc
import proto.task_pb2 as pb2

from master import MANAGE

class TaskClient(object):

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        #Change to a secure channel
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))
        self.stub = pb2_grpc.SendTaskStub(self.channel)

    def getResultTask(self, task, arg):
        message = pb2.Task(task=task, arg=arg)
        print(message)

        return self.stub.GetServerResponse(message)

def cli(client):
    opt = 0
    c_workers = int(client.getResultTask(task='numberWorkers', arg=None).result)
    while True:
        print("Press 0 & enter to Exit")
        print("Press 1 & enter to Select tasks\n")
        print('Now you have: [',c_workers,'] Workers, to be able to execute any task, you must have at least one')
        print("Manage Workers:")
        print("\tlistWorkers\n\tremoveWorker\n\tcreateWorker\n")
        opt = input("What do you want to do? ")

        if opt == '0': break
        if opt not in MANAGE:
            print("ERROR: does not exist")

        else:
            arg = None
            if MANAGE[opt] == 'removeWorker':
                print('removeWorker needs an argument, it must be the worker ID')
                arg = (input("workerID: "))
                c_workers = c_workers-1

            elif MANAGE[opt] == 'createWorker': c_workers += 1
            result = client.getResultTask(task=opt, arg=arg)
            print(f"\n\t{result}\n")
        if opt == 1:
            if c_workers == 0:
                print('ERROR: Workers cannot be 0')
                break

            while True:
                print("Press 0 & enter to Exit and Manage workers")
                print("Available tasks:")
                print("\tcountingWords\n\twordCount\n")
                opt = input("Task name: >> ")

                if opt == '0': break
                file = input("URL: >> ")
                result = (client.getResultTask(task=opt, arg=file))
                print("result:",result.result,"\n")


def test(client):
    assert client.getResultTask(task='numberWorkers', arg=None).result          == '0'
    assert client.getResultTask(task='listWorkers', arg=None).result            == '{}'

    assert client.getResultTask(task='createWorker', arg=None).result           == '0'
    assert client.getResultTask(task='removeWorker', arg='0').result            == 'True'
   
    assert client.getResultTask(task='numberWorkers', arg=None).result          == '0'
    assert client.getResultTask(task='createWorker', arg=None).result           == '1'
    assert client.getResultTask(task='createWorker', arg=None).result           == '2'
    assert client.getResultTask(task='createWorker', arg=None).result           == '3'

    assert client.getResultTask(task='countingWords', arg='http://localhost:8000/tests/test_word_count.txt http://localhost:8000/tests/test_word_count.txt').result             == '8'
    assert client.getResultTask(task='countingWords', arg='http://localhost:8000/tests/test_word_count.txt http://localhost:8000/tests/test2.txt').result                       == '9'
    assert client.getResultTask(task='countingWords', arg='http://localhost:8000/tests/test2.txt http://localhost:8000/tests/test2.txt').result                 	            == '10'
    assert client.getResultTask(task='countingWords', arg='http://localhost:8000/tests/test2.txt http://localhost:8000/tests/test2.txt http://localhost:8000/tests/test2.txt http://localhost:8000/tests/test2.txt').result           == '20'

    assert client.getResultTask(task='wordCount', arg='http://localhost:8000/tests/test_word_count.txt').result           == "{'foo': 2, 'barra': 2}"
    assert client.getResultTask(task='wordCount', arg='http://localhost:8000/tests/test_word_count.txt http://localhost:8000/tests/test_word_count.txt').result           == "{'foo': 4, 'barra': 4}"
    assert client.getResultTask(task='wordCount', arg='http://localhost:8000/tests/test_word_count.txt http://localhost:8000/tests/test_word_count.txt http://localhost:8000/tests/test_word_count.txt').result           == "{'foo': 6, 'barra': 6}"

if __name__ == '__main__':
    client = TaskClient()
    #cli(client)
    test(client)


    