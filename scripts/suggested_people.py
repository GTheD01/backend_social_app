import django
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'social_app_backend.settings')
django.setup()

from users.models import UserAccount

users = UserAccount.objects.all()

for user in users:

    user.suggested_people.clear()

    print("Find people for: ", user)

    for person in user.following.all():
        print("Follows: ", person)

        for followingfollows in person.following.all():
            if followingfollows not in user.following.all() and followingfollows != user:
                user.suggested_people.add(followingfollows)
    user.save()                

