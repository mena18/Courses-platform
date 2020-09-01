# Generated by Django 3.1 on 2020-09-01 08:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user_registration',
            unique_together={('user', 'course')},
        ),
        migrations.AlterIndexTogether(
            name='user_registration',
            index_together={('user', 'course')},
        ),
    ]
