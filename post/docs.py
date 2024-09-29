from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Schema for post_list view
post_list_schema = swagger_auto_schema(
    method='get',
    operation_id='post_list',
    operation_description="Retrieve a list of posts for the authenticated user.",
    responses={
        200: openapi.Response(
            description="A paginated list of posts",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'next': openapi.Schema(type=openapi.TYPE_STRING, description="URL to the next page of results"),
                    'previous': openapi.Schema(type=openapi.TYPE_STRING, description="URL to the previous page of results"),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the post"),
                                'title': openapi.Schema(type=openapi.TYPE_STRING, description="Title of the post"),
                                'content': openapi.Schema(type=openapi.TYPE_STRING, description="Content of the post"),
                                'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Creation date of the post"),
                            }
                        ),
                    ),
                },
            ),
        ),
        401: "Unauthorized",
        403: "Forbidden"
    },
)

# Schema for post_list_profile view
post_list_profile_schema = swagger_auto_schema(
    method='get',
    operation_id='post_list_profile',
    operation_description="Retrieve posts for a specific user by username.",
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_PATH, description="The username of the user", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(
            description="A list of posts created by the specified user",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the post"),
                        'title': openapi.Schema(type=openapi.TYPE_STRING, description="Title of the post"),
                        'content': openapi.Schema(type=openapi.TYPE_STRING, description="Content of the post"),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Creation date of the post"),
                    }
                ),
            ),
        ),
        404: "User not found"
    },
)

# Schema for post_detail view
post_detail_schema = swagger_auto_schema(
    method='get',
    operation_id='post_detail',
    operation_description="Retrieve the details of a specific post by ID.",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the post", type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(
            description="The details of the specified post",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the post"),
                    'title': openapi.Schema(type=openapi.TYPE_STRING, description="Title of the post"),
                    'content': openapi.Schema(type=openapi.TYPE_STRING, description="Content of the post"),
                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Creation date of the post"),
                }
            ),
        ),
        404: "Post not found"
    },
)

# Schema for post_delete view
post_delete_schema = swagger_auto_schema(
    method='delete',
    operation_id='post_delete',
    operation_description="Delete a specific post by ID.",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the post", type=openapi.TYPE_INTEGER),
    ],
    responses={
        204: "Post deleted",
        403: "Forbidden"
    },
)

# Schema for create_post view
create_post_schema = swagger_auto_schema(
    method='post',
    operation_id='create_post',
    operation_description="Create a new post.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="Title of the post"),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description="Content of the post"),
            'images': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="Images to attach to the post"),
        },
        required=['title', 'content']
    ),
    responses={
        201: openapi.Response(
            description="Post created successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the created post"),
                    'title': openapi.Schema(type=openapi.TYPE_STRING, description="Title of the post"),
                    'content': openapi.Schema(type=openapi.TYPE_STRING, description="Content of the post"),
                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Creation date of the post"),
                }
            ),
        ),
        400: "Body text or at least one image attachment is required."
    },
)

# Schema for like_post view
like_post_schema = swagger_auto_schema(
    method='post',
    operation_id='like_post',
    operation_description="Like or unlike a specific post by ID.",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the post", type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(
            description="Post liked or unliked successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the post"),
                    'likes_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Updated likes count"),
                }
            ),
        ),
        404: "Post not found"
    },
)

# Schema for comment_post view
comment_post_schema = swagger_auto_schema(
    method='post',
    operation_id='comment_post',
    operation_description="Comment on a specific post.",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the post", type=openapi.TYPE_INTEGER),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'body': openapi.Schema(type=openapi.TYPE_STRING, description="Body text of the comment"),
        },
        required=['body']
    ),
    responses={
        201: openapi.Response(
            description="Comment created successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the comment"),
                    'body': openapi.Schema(type=openapi.TYPE_STRING, description="Body text of the comment"),
                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Creation date of the comment"),
                }
            ),
        ),
        400: "Body text required"
    },
)

# Schema for delete_comment view
delete_comment_schema = swagger_auto_schema(
    method='post',
    operation_id='delete_comment',
    operation_description="Delete a comment from a post.",
    manual_parameters=[
        openapi.Parameter('postId', openapi.IN_PATH, description="The ID of the post", type=openapi.TYPE_INTEGER),
        openapi.Parameter('commentId', openapi.IN_PATH, description="The ID of the comment", type=openapi.TYPE_INTEGER),
    ],
    responses={
        204: "Comment deleted",
        403: "Forbidden"
    },
)

# Schema for save_post view
save_post_schema = swagger_auto_schema(
    method='post',
    operation_id='save_post',
    operation_description="Save or unsave a specific post by ID.",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="The ID of the post", type=openapi.TYPE_INTEGER),
    ],
    responses={
        200: openapi.Response(
            description="Post saved or unsaved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the post"),
                    'saved': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Whether the post was saved or unsaved"),
                }
            ),
        ),
        404: "Post not found"
    },
)

# Schema for saved_posts view
saved_posts_schema = swagger_auto_schema(
    method='get',
    operation_id='saved_posts',
    operation_description="Retrieve saved posts for the authenticated user.",
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_PATH, description="The username of the user", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(
            description="A list of saved posts",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the post"),
                        'title': openapi.Schema(type=openapi.TYPE_STRING, description="Title of the post"),
                        'content': openapi.Schema(type=openapi.TYPE_STRING, description="Content of the post"),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Creation date of the post"),
                    }
                ),
            ),
        ),
        403: "Forbidden"
    },
)

# Schema for get_popular_post view
get_popular_post_schema = swagger_auto_schema(
    method='get',
    operation_id='get_popular_post',
    operation_description="Retrieve the popular post.",
    responses={
        200: openapi.Response(
            description="The popular post",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the popular post"),
                    'title': openapi.Schema(type=openapi.TYPE_STRING, description="Title of the popular post"),
                    'content': openapi.Schema(type=openapi.TYPE_STRING, description="Content of the popular post"),
                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Creation date of the popular post"),
                }
            ),
        ),
        404: "Popular post not found"
    },
)
