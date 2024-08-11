from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from post.models import Post

from .forms import PostForm
from .serializers import PostSerialzier
# Create your views here.


@api_view(["GET"])
def post_list(request):
    user = request.user

    posts = Post.objects.filter(created_by=user.id)

    serializer = PostSerialzier(posts, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def post_detail(request, id):
    user = request.user

    post = Post.objects.filter(created_by=user.id).get(pk=id)

    serializer = PostSerialzier(post)

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
    form = PostForm(request.POST)
    
    if form.is_valid():

        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
    
        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerialzier(post)

        return Response(serializer.data)
    else:
        return Response({'error': "Failed to create post"})
    
