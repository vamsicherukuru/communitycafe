# Generated by Django 3.1.4 on 2021-05-29 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cc', '0014_auto_20210416_1310'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiveBackReg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_photo', models.ImageField(blank=True, null=True, upload_to='give_back_photos')),
                ('resource_description', models.CharField(blank=True, max_length=250, null=True)),
                ('phone', models.CharField(max_length=10)),
                ('resource', models.CharField(choices=[('Share', 'Share'), ('Lend', 'Lend'), ('Recycle', 'Recycle'), ('Donate', 'Donate')], max_length=100)),
                ('owner_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
