# Generated by Django 4.0.2 on 2022-03-11 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_tutorobject'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('EMAIL', 'Email'), ('PHONE', 'Phone'), ('SITE', 'Website'), ('VK', 'Vkontakte'), ('INSTAGRAM', 'Instagram'), ('OTHER', 'Others')], max_length=9)),
                ('value', models.CharField(max_length=256)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='clubs.clubmodel')),
            ],
        ),
    ]