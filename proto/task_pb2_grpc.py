# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import task_pb2 as proto_dot_task__pb2


class SendTaskStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetServerResponse = channel.unary_unary(
                '/task.SendTask/GetServerResponse',
                request_serializer=proto_dot_task__pb2.Task.SerializeToString,
                response_deserializer=proto_dot_task__pb2.TaskResponse.FromString,
                )


class SendTaskServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetServerResponse(self, request, context):
        """A simple RPC.

        Obtains the MessageResponse at a given position.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SendTaskServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetServerResponse': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServerResponse,
                    request_deserializer=proto_dot_task__pb2.Task.FromString,
                    response_serializer=proto_dot_task__pb2.TaskResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'task.SendTask', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SendTask(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetServerResponse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/task.SendTask/GetServerResponse',
            proto_dot_task__pb2.Task.SerializeToString,
            proto_dot_task__pb2.TaskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
