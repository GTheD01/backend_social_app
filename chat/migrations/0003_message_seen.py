# Generated by Django 5.0.7 on 2024-08-25 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_message_options_alter_conversation_modified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
