# Generated by Django 3.1.4 on 2021-04-16 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0012_businessreg_business_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantitems',
            name='available_today',
            field=models.BooleanField(default=True),
        ),
    ]
