# Generated by Django 4.0.2 on 2022-02-05 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feed", "0002_alter_feedmodel_address_alter_feedmodel_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedmodel",
            name="type",
            field=models.CharField(
                choices=[
                    ("ARTICLE", "Article"),
                    ("ARTICLE_SPONSORED", "Sponsored article"),
                    ("EVENT", "Event"),
                    ("EVENT_SPONSORED", "Sponsored event"),
                ],
                max_length=17,
            ),
        ),
    ]