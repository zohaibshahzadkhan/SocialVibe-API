# Generated by Django 5.0.6 on 2024-06-17 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='deleted',
        ),
    ]
