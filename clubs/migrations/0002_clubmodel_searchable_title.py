# Generated by Django 4.0.2 on 2022-02-28 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubmodel',
            name='searchable_title',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]