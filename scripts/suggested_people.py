import django
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'social_app_backend.settings')
django.setup()

from users.models import UserAccount

# users = UserAccount.objects.all()
users = UserAccount.objects.prefetch_related('following', 'suggested_people')
print(users)
for user in users:


    user.suggested_people.clear()


    print("Find people for: ", user)
    user_following = user.following.all()


    followers_of_following = UserAccount.objects.filter(
        followers__in=user_following
    ).exclude(pk=user.pk).exclude(pk__in=user_following).distinct()


    user.suggested_people.add(*followers_of_following)
    print(f"Suggested people for {user}: {followers_of_following}")
    

    user.save()                

