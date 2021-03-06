# Generated by Django 3.0.6 on 2020-05-20 14:58
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("reporting", "0005_auto_20200520_1438"),
    ]

    operations = [
        migrations.AlterField(
            model_name="encampment",
            name="location",
            field=models.CharField(
                help_text="An intersection or address. Adding a city/state can help accuracy.",
                max_length=250,
            ),
        ),
        migrations.AlterField(
            model_name="encampment",
            name="name",
            field=models.CharField(
                help_text="A descriptive name for the encampment, which may be based on the address.",
                max_length=100,
            ),
        ),
    ]
