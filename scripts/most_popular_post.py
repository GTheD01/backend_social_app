import django
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'social_app_backend.settings')
django.setup()

from post.models import Post

posts = Post.objects.all()
