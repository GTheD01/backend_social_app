import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from PIL import Image

# from post.models import Post


# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")


        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


        return user


def avatar_upload_to(instance, filename):
    return f"avatars/{instance.username}/{filename}"

class UserAccount(AbstractBaseUser, PermissionsMixin):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="followers_set")
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="following_set")
    mfa_enabled = models.BooleanField(default=False)

    saved_posts = models.ManyToManyField('post.Post', blank=True)

    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)

    suggested_people = models.ManyToManyField('self')

    posts_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username', 'full_name']

    def __str__(self) -> str:
        return self.email

    def get_avatar(self):
        if (self.avatar):
            return settings.WEBSITE_URL +  self.avatar.url
        else: 
            return settings.WEBSITE_URL + settings.DEFAULT_USER_IMAGE_PATH
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 100 or img.width > 100:
                size = (100, 100)
                img.thumbnail(size)
                img.save(self.avatar.path)
    