import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from post.models import Post, Like, Comment
from users.models import UserAccount
from django.db.models import Q

from notifications.utilities import create_notification

from .forms import PostForm, AttachmentForm
from .serializers import PostSerializer, CommentSerializer
from .paginations import PostCursorPagination
# Create your views here.


@api_view(["GET"])
def post_list(request):
    user = request.user
    users =[user]
    for u in user.following.all():
        users.append(u)
    posts = Post.objects.filter(created_by__in=users)

    paginator = PostCursorPagination()

    result_page = paginator.paginate_queryset(posts, request)

    serializer = PostSerializer(result_page, many=True, context={'request':request})

    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def post_list_profile(request, username):
    user = UserAccount.objects.get(username=username)
    posts = Post.objects.filter(created_by=user.id)

    serializer = PostSerializer(posts, many=True, context={"request": request})

    return Response(serializer.data)


@api_view(['GET'])
def post_detail(request, id):
    try:
        post = Post.objects.get(pk=id)

        serializer = PostSerializer(post, context={'request': request})
    except:
        return Response({'error': "Post not found"})

    return Response(serializer.data)


@api_view(['DELETE'])
def post_delete(request, id):
    user = request.user

    post = Post.objects.filter(created_by=user.id).get(pk=id)
    if post.attachments:
        for attachment in post.attachments.all():
            file_path = attachment.image.path # getting file path(not needed in production since we store images elsewhere)
            attachment.delete()

            # Deleting uploaded files (not needed this in production)
            if os.path.isfile(file_path):
                os.remove(file_path)
    
    # Using this approach because ManyToManyField cannot have on_delete=CASCADE
    # Another approach will be to create separate model that connects like model and post model through that separate model with ForeignKeys
    if post.likes:
        for like in post.likes.all():
            like.delete()


    post.delete()

    # WORKS
    user.posts_count = user.posts_count - 1
    user.save()

    return Response({'message': "Post deleted"})

@api_view(['POST'])
def create_post(request):
    form = PostForm(request.POST, request.FILES)

    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()
    

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post, context={'request':request})

        return Response(serializer.data)
    elif attachment:
        post = Post.objects.create(created_by=request.user, body="")
        post.save()
        post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)
        
        return Response(serializer.data)
    else:
        return Response({'error': "Body text or image attachment required."}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def like_post(request, id):
    post = Post.objects.get(pk=id)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        serializer = PostSerializer(post, context={"request":request})

        if post.created_by != request.user:
            notification = create_notification(request, 'post_liked', post_id=id)

        return Response(serializer.data)
    else:
        like = post.likes.get(created_by=request.user)
        post.likes_count = post.likes_count - 1
        post.likes.remove(like)
        like.delete()
        post.save()
        serializer = PostSerializer(post, context={"request":request})
        return Response(serializer.data)
    

@api_view(['POST'])
def comment_post(request, id):
    body = request.data.get("body")
    if not body:
        return Response({"error": "Body text required"}, status=status.HTTP_400_BAD_REQUEST)
    comment = Comment.objects.create(body=body, created_by=request.user)

    post = Post.objects.get(pk=id)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    if post.created_by != request.user:
        notification = create_notification(request, 'post_commented', post_id=id)

    serializer = CommentSerializer(comment, context={"request":request})

    return Response(serializer.data)


@api_view(['POST'])
def delete_comment(request, postId, commentId):
    post = Post.objects.get(pk=postId)
    

    if post.created_by == request.user:
        comment = Comment.objects.get(pk=commentId)
    else:
        comment = Comment.objects.get(created_by=request.user, pk=commentId)

    post.comments_count = post.comments_count - 1
    post.comments.remove(comment)
    comment.delete()
    post.save()

    return Response({"message": "Comment deleted"})


@api_view(['POST'])
def save_post(request, id):
    post = Post.objects.get(pk=id)
    user = request.user
    if not user.saved_posts.filter(pk=post.id).exists():
        user.saved_posts.add(post)

    else:
        user.saved_posts.remove(post)
    serializer = PostSerializer(post, context={'request':request})
    return Response(serializer.data)

    

@api_view(['GET'])
def saved_posts(request, username):
    user = request.user
    curr_user = UserAccount.objects.get(username=username)

    if user == curr_user:
        saved_posts_list = user.saved_posts
        serializer = PostSerializer(saved_posts_list, many=True, context={'request': request})

        return Response(serializer.data)
    else: 
        return Response(status=status.HTTP_403_FORBIDDEN)
