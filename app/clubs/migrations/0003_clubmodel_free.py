# Generated by Django 4.0.2 on 2022-03-11 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_remove_clubmodel_price_priceobject'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubmodel',
            name='free',
            field=models.BooleanField(default=False),
        ),
    ]
