import django
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'social_app_backend.settings')
django.setup()

from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from post.models import Post

now = timezone.now()
last_24_hours = now - timedelta(hours=24)

posts = Post.objects.filter(likes__created_at__gte=last_24_hours).annotate(like_count=Count('likes')).order_by('-like_count')

top_post = posts[:1]
print(top_post)