# Generated by Django 4.2.6 on 2023-10-24 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tripobeatApp", "0002_alter_category_cost"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="access",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="category",
            name="cancel",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="category",
            name="departure_details",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="category",
            name="exclusions",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="category",
            name="inclusions",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="category",
            name="return_details",
            field=models.TextField(default=""),
        ),
    ]