# Generated by Django 3.1.4 on 2021-04-10 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0004_confirmedorders'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantitems',
            name='display_picture',
            field=models.ImageField(blank=True, null=True, upload_to='food_images'),
        ),
    ]
