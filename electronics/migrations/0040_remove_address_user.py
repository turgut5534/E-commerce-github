# Generated by Django 3.2.8 on 2021-11-27 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0039_address_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
    ]
