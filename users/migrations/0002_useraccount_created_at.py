# Generated by Django 5.0.7 on 2024-07-14 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
