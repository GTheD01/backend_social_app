# Generated by Django 5.0.7 on 2024-10-04 10:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0008_alter_post_likes"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Like",
        ),
    ]
