# Generated by Django 5.0.7 on 2024-10-14 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0009_delete_like"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="shared",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="post.post",
            ),
        ),
    ]
