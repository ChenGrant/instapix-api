from django.urls import path
from . import views

urlpatterns = [
    path("photo-list", views.photo_list, name="photo-list"),
    path("photo-create", views.photo_create, name="photo-create"),
    path("post-generate", views.post_generate, name="post-generate"),
]
