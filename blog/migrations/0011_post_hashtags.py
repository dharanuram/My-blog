# Generated by Django 5.0.6 on 2024-07-31 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_remove_comment_reply_to_comment_parent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.TextField(blank=True, help_text='Space-separated list of hashtags'),
        ),
    ]