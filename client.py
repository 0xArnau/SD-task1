import grpc
import proto.task_pb2_grpc as pb2_grpc
import proto.task_pb2 as pb2

class TaskClient(object):

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        #Change to a secure channel
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))

        self.stub = pb2_grpc.SendTaskStub(self.channel)

    def getResultTask(self, task, file):
        message = pb2.Task(task=task, file=file)
        print(message)

        return self.stub.GetServerResponse(message)

class Worker(object):

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        #Change to a secure channel
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))

        self.stubW = pb2_grpc.ManageWorkersStub(self.channel)

    def manageWorkers(self, manage):
        message = pb2.Workers(manage=manage)
        print(message)

        return self.stubW.GetWorkersResponse(message)


def cli(client, worker):
    while True:
        print("Manage Workers")
        manage = input("Operations...")
        result = (worker.manageWorkers(manage=manage))
        print(result)

    while True:
        print("Available tasks:")
        print("\tcountingWords\n\twordCount\n")
        task = input("Task name: >> ")
        file = input("URL: >> ")
        result = (client.getResultTask(task=task, file=file))
        print(result)

def loop(client, task, filename, n: int):
    result = []
    for _ in range(n):
        result.append((client.getResultTask(task=task, file=filename)))
    return result

if __name__ == '__main__':
    client = TaskClient()
    worker = Worker()
    cli(client, worker)
    #result = loop(client,'wordCount','http://localhost:8000/test_word_count.txt',1)
    for x in result:
        print(x)
    