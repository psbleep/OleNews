# Generated by Django 2.0.3 on 2018-05-13 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_site', '0009_auto_20180512_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspost',
            name='users_liked',
            field=models.ManyToManyField(blank=True, related_name='news_posts_liked', to='news_site.Profile'),
        ),
    ]
