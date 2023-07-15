from rest_framework.decorators import api_view
from rest_framework.response import Response
import grpc
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../protos")))
import user_pb2_grpc
import user_pb2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../protos")))
import photo_pb2_grpc
import photo_pb2


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../protos")))
import post_pb2_grpc
import post_pb2


def authenticate_required(f):
    def decorator(request, *args, **kwargs):
        firebase_id_token = request.META.get("HTTP_AUTHORIZATION")
        if not firebase_id_token:
            return Response("Authentication Required")
        with grpc.insecure_channel(os.environ["USERS_SERVER_ADDRESS"]) as channel:
            stub = user_pb2_grpc.UserStub(channel)
            response = stub.AuthenticateUser(
                user_pb2.AuthenticateUserRequest(firebase_id_token=firebase_id_token)
            )
        if not response.uid:
            return Response("Authentication failed")
        return f(request, *args, **kwargs, uid=response.uid)

    return decorator


# -------------------- photos --------------------
@api_view(["GET"])
@authenticate_required
def photo_list(request, uid):
    with grpc.insecure_channel(os.environ["PHOTOS_SERVER_ADDRESS"]) as channel:
        stub = photo_pb2_grpc.PhotoServiceStub(channel)
        # get photos from photo microservice
        responses = stub.GetPhotos(photo_pb2.GetPhotosRequest(uid=uid))
        photos = [
            {
                "id": response.photo.id,
                "uid": response.photo.uid,
                "name": response.photo.name,
                "content_type": response.photo.content_type,
                "src": response.photo.src,
            }
            for response in responses
        ]
    return Response(photos)


@api_view(["POST"])
@authenticate_required
def photo_create(request, uid):
    # unpack photos from client request
    photos = [
        {
            "uid": uid,
            "name": file.name,
            "content": file.read(),
            "content_type": file.content_type,
        }
        for file in request.FILES.values()
    ]

    # send photos to photo microservice
    with grpc.insecure_channel(os.environ["PHOTOS_SERVER_ADDRESS"]) as channel:
        stub = photo_pb2_grpc.PhotoServiceStub(channel)
        response = stub.UploadPhotos(
            photo_pb2.UploadPhotoRequest(photo=photo) for photo in photos
        )

    # respond to client
    return Response({"uploaded": response.uploaded})


# -------------------- posts --------------------
@api_view(["POST"])
@authenticate_required
def post_generate(request, uid):
    prompt = json.loads(request.body)["prompt"]

    # send prompt to post microservice
    with grpc.insecure_channel(os.environ["POSTS_SERVER_ADDRESS"]) as channel:
        stub = post_pb2_grpc.PostServiceStub(channel)
        responses = stub.GeneratePosts(
            post_pb2.GeneratePostsRequest(uid=uid, prompt=prompt)
        )
        posts = [{"photo_src": response.post.photo_src} for response in responses]

    return Response(posts)
