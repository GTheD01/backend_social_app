from django.urls import path
from .views import post_list, create_post, post_detail, post_delete, like_post, save_post, saved_posts, post_list_profile, comment_post, delete_comment, get_popular_post

urlpatterns = [
    path("", post_list, name='post_list'),
    path("profile/<str:username>/", post_list_profile, name="post_list_profile"),
    path("<uuid:id>/", post_detail, name='post_detail'),
    path("delete/<uuid:id>/", post_delete),
    path("create/", create_post, name='create_post'),
    path("like/<uuid:id>/", like_post, name="post_like"),
    path("comment/<uuid:id>/", comment_post, name="post_comment"),
    path("<uuid:postId>/comment/delete/<uuid:commentId>/", delete_comment, name="comment_delete"),
    path("save/<uuid:id>/", save_post, name="post_save"),
    path('saved/<str:username>/', saved_posts, name='saved_posts'),
    path("popular-post/", get_popular_post, name="popular-post"),
]