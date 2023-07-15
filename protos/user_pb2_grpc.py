# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import user_pb2 as user__pb2


class UserStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AuthenticateUser = channel.unary_unary(
                '/User/AuthenticateUser',
                request_serializer=user__pb2.AuthenticateUserRequest.SerializeToString,
                response_deserializer=user__pb2.AuthenticateUserResponse.FromString,
                )


class UserServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AuthenticateUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AuthenticateUser': grpc.unary_unary_rpc_method_handler(
                    servicer.AuthenticateUser,
                    request_deserializer=user__pb2.AuthenticateUserRequest.FromString,
                    response_serializer=user__pb2.AuthenticateUserResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'User', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class User(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AuthenticateUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/User/AuthenticateUser',
            user__pb2.AuthenticateUserRequest.SerializeToString,
            user__pb2.AuthenticateUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
