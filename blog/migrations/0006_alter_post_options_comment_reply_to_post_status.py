# Generated by Django 5.0.6 on 2024-07-23 10:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': [('can_edit_posts', 'Can edit posts'), ('can_publish_posts', 'Can publish posts'), ('can_put_on_hold', 'Can put posts on hold')]},
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='blog.comment'),
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('on_hold', 'On Hold'), ('published', 'Published')], default='draft', max_length=20),
        ),
    ]