# Generated by Django 4.2.6 on 2023-11-09 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_remove_details_first_name_remove_details_last_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="details",
            name="gender",
            field=models.CharField(default="other", max_length=10),
        ),
    ]
