# Generated by Django 5.0.7 on 2024-08-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterField(
            model_name='conversation',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
