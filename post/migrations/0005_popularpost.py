# Generated by Django 5.0.7 on 2024-09-23 19:35

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0004_post_comments_count_comment_post_comments"),
    ]

    operations = [
        migrations.CreateModel(
            name="PopularPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "calculated_at",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2024,
                            9,
                            23,
                            19,
                            35,
                            18,
                            205829,
                            tzinfo=datetime.timezone.utc,
                        )
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="post.post"
                    ),
                ),
            ],
        ),
    ]
