# Generated by Django 4.0.2 on 2022-03-13 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('profile_photo', models.CharField(default=None, max_length=1024, null=True)),
            ],
        ),
    ]
