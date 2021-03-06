# Generated by Django 4.0.2 on 2022-03-13 03:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationmodel',
            name='id',
        ),
        migrations.AlterField(
            model_name='organizationmodel',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='owned_organization', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
