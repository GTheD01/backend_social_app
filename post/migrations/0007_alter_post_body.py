# Generated by Django 5.0.7 on 2024-10-03 21:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0006_alter_popularpost_calculated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="body",
            field=models.TextField(blank=True, null=True),
        ),
    ]
