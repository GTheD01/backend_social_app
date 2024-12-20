import django
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'social_app_backend.settings')
django.setup()

from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from post.models import Post, PopularPost

now = timezone.now()
last_24_hours = now - timedelta(hours=24)

top_post = (
    Post.objects.filter(created_at__gte=last_24_hours)  # Posts created in the last 24 hours
    .annotate(like_count=Count('likes'))  # Count the number of likes per post
    .order_by('-like_count')  # Order by the number of likes (descending)
    .first()  # Get the post with the most likes
)


if top_post:
    popular_post, created = PopularPost.objects.update_or_create(
        id=2,
        defaults={"post": top_post, "calculated_at": now}
    )

    action_taken = 'created' if created else 'updated'
    print(f"Popular post {action_taken}: {popular_post.id} for post: {top_post.id}")

else:
    print("No popular post found in the last 24 hours.")
