# Generated by Django 4.0.2 on 2022-03-11 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('districts', '0001_initial'),
        ('clubs', '0006_clubmodel_latitude_clubmodel_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubmodel',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='districts.districtmodel'),
        ),
    ]
