# Generated by Django 3.2.8 on 2021-11-27 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0041_auto_20211127_2322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='virtualcard',
            name='user',
        ),
    ]