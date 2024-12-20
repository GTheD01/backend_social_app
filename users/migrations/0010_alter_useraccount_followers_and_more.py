# Generated by Django 5.0.7 on 2024-08-11 01:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_useraccount_followers_useraccount_followers_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
