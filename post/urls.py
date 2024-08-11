from django.urls import path
from .views import post_list, create_post, post_detail, post_delete, like_post

urlpatterns = [
    path("", post_list, name='post_list'),
    path("<uuid:id>/", post_detail, name='post_detail'),
    path("delete/<uuid:id>/", post_delete),
    path("create/", create_post, name='post_list'),
    path("like/<uuid:id>/", like_post, name="post_like")
]