from django.urls import path
from .views import post_list, create_post, post_detail, post_delete, like_post, save_post, saved_posts

urlpatterns = [
    path("", post_list, name='post_list'),
    path("<uuid:id>/", post_detail, name='post_detail'),
    path("delete/<uuid:id>/", post_delete),
    path("create/", create_post, name='post_list'),
    path("like/<uuid:id>/", like_post, name="post_like"),
    path("save/<uuid:id>/", save_post, name="post_save"),
    path('saved/', saved_posts, name='saved_posts')
]