# Generated by Django 3.1.4 on 2021-04-10 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0005_restaurantitems_display_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessreg',
            name='caption',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]