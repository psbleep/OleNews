# Generated by Django 2.0.2 on 2018-05-21 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_site', '0013_remove_profile_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_consent',
            field=models.BooleanField(default=False),
        ),
    ]
