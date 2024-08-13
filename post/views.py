import os
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from post.models import Post, PostAttachment, Like

from .forms import PostForm, AttachmentForm
from .serializers import PostSerializer, PostAttachmentSerializer
# Create your views here.


@api_view(["GET"])
def post_list(request):
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True, context={'request':request})

    return Response(serializer.data,)


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

        serializer = PostSerializer(post)

        return Response(serializer.data)
    else:
        return Response({'error': "Failed to create post"})
    

@api_view(['POST'])
def like_post(request, id):
    post = Post.objects.get(pk=id)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        return Response({'message': "liked"})
    else:
        like = post.likes.get(created_by=request.user)
        print(like)
        post.likes_count = post.likes_count - 1
        post.likes.remove(like)
        like.delete()
        post.save()
        return Response({'message': "like removed"})
