# Generated by Django 3.2.8 on 2021-11-25 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0022_auto_20211125_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='expiry',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
