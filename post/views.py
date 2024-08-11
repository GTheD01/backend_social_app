from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from post.models import Post, PostAttachment

from .forms import PostForm, AttachmentForm
from .serializers import PostSerializer, PostAttachmentSerializer
# Create your views here.


@api_view(["GET"])
def post_list(request):
    user = request.user

    posts = Post.objects.filter(created_by=user.id)

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def post_detail(request, id):
    user = request.user

    post = Post.objects.filter(created_by=user.id).get(pk=id)

    serializer = PostSerializer(post)

    return Response(serializer.data)


@api_view(['DELETE'])
def post_delete(request, id):
    user = request.user

    post = Post.objects.filter(created_by=user).get(pk=id)
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
    print(attachment_form)

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
    
