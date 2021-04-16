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

def cli(client):
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
    #cli(client)
    result = loop(client,'wordCount','http://localhost:8000/test_word_count.txt',1)
    for x in result:
        print(x)
    