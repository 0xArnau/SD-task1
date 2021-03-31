import grpc
import task_pb2_grpc as pb2_grpc
import task_pb2 as pb2

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
        
if __name__ == '__main__':
    client = TaskClient()
    result = []
    for _ in range(1):
        #result.append(client.getResultTask(task='countingWords', file='test_word_count.txt'))
        result.append(client.getResultTask(task='wordCount', file='test_word_count.txt'))
    

    for x in result:
        print(x)