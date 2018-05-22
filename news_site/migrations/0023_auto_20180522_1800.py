# Generated by Django 2.0.2 on 2018-05-22 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news_site', '0022_auto_20180522_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspost',
            name='user',
            field=models.ForeignKey(default=None, limit_choices_to={'is_active': True, 'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]