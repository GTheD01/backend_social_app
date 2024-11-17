from rest_framework.generics import (ListCreateAPIView, 
                                    RetrieveUpdateDestroyAPIView, 
                                    GenericAPIView, 
                                    ListAPIView, 
                                    )
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth import get_user_model

from post.models import Post, Comment, PostAttachment, PopularPost
from .serializers import PostSerializer, CommentSerializer
from .paginations import PostCursorPagination
from .permissions import IsOwnerOrReadOnly
from notifications.utilities import create_notification

UserAccount = get_user_model()


class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    pagination_class = PostCursorPagination

    def get_queryset(self):
        user = self.request.user
        users = [user] + list(user.following.all())
        return Post.objects.select_related('created_by').filter(created_by__in=users)

    def perform_create(self, serializer):
        images = self.request.FILES.getlist('image')
        user = self.request.user
        post = serializer.save(created_by=user)

        if images:
            for image in images:
                attachment = PostAttachment.objects.create(created_by=user, image=image)
                post.attachments.add(attachment)
        
        user.posts_count +=1
        user.save()

        return post


class RetrieveUpdateDeletePostView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'


class RetrieveUserPostsView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(UserAccount, username=username)
        return Post.objects.select_related('created_by').filter(created_by=user)
        

class LikePostApiView(GenericAPIView):
    queryset = Post.objects.select_related('created_by').all()
    serializer_class = PostSerializer
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.likes_count -= 1
            post.save()

            return Response({'message': 'Liked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            post.likes_count += 1

            if post.created_by != request.user:
                create_notification(request, 'post_liked', post_id=post.id)
            post.save()
            return Response({"message": "liked"}, status=status.HTTP_200_OK)
    

class CommentPostView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg=['post_id', 'comment_id']

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['postId']
        body = request.data.get("body")

        if not body:
            return Response({"error": "Body text required."}, status=status.HTTP_400_BAD_REQUEST)

        post = get_object_or_404(Post, id=post_id)
        comment = Comment.objects.create(body=body, created_by=request.user)

        post.comments.add(comment)
        post.comments_count += 1
        post.save()

        if post.created_by != request.user:
            create_notification(request, "post_commented", post_id=post_id)
        
        return Response(status=status.HTTP_201_CREATED)


    def delete(self, request, *args, **kwargs):
        post_id = self.kwargs['postId']
        comment_id = self.kwargs['commentId']
        post = get_object_or_404(Post, pk=post_id)
        if post.created_by == request.user:
            comment = get_object_or_404(Comment, pk=comment_id)
        else:
            comment = get_object_or_404(Comment, created_by=request.user, pk=comment_id)

        post.comments.remove(comment)
        post.comments_count -= 1
        comment.delete()
        post.save()

        return Response({"message": "Comment deleted"}, status=status.HTTP_200_OK)


class SavePostApiView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['postId']
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if not user.saved_posts.filter(id=post_id).exists():
            user.saved_posts.add(post)
            message = "Post saved"
        else:
            user.saved_posts.remove(post)
            message = "Post removed from saved"
        
        return Response({"message": message})


class RetrieveUserSavedPostsView(GenericAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(UserAccount.objects.prefetch_related('saved_posts'), username=username)
        return user.saved_posts.select_related('created_by')

    def get(self, request, *args, **kwargs):
        username = self.kwargs['username']
        queryset = self.get_queryset()

        if request.user.username == username:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        


class RetrievePopularPost(GenericAPIView):
    queryset = PopularPost.objects.all().select_related('post')
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        popular_post = self.queryset.last()
        if popular_post:
            post = popular_post.post
            serializer = self.get_serializer(post)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
