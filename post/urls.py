from django.urls import path
from .views import (PostListCreateView, 
                    RetrieveUpdateDeletePostView, 
                    LikePostApiView, 
                    RetrieveUserPostsView, 
                    CommentPostView,
                    SavePostApiView,
                    RetrieveUserSavedPostsView,
                    RetrievePopularPost)

urlpatterns = [
    path("", PostListCreateView.as_view(), name='post_list_create'),
    path("<uuid:id>/", RetrieveUpdateDeletePostView.as_view(), name='post_detail_update_delete'),
    path("like/<uuid:id>/", LikePostApiView.as_view(), name="post_like"),
    path("profile/<str:username>/", RetrieveUserPostsView.as_view(), name="post_list_profile"),
    path("comment/<uuid:postId>/", CommentPostView.as_view(), name="post_comment"),
    path("<uuid:postId>/comment/delete/<uuid:commentId>/", CommentPostView.as_view(), name="comment_delete"),
    path("save/<uuid:postId>/", SavePostApiView.as_view(), name="post_save"),
    path('saved/<str:username>/', RetrieveUserSavedPostsView.as_view(), name='saved_posts'),
    path("popular-post/", RetrievePopularPost.as_view(), name="popular-post"),
    
]