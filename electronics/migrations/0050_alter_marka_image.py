# Generated by Django 3.2.8 on 2021-12-01 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0049_alter_orderdetail_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marka',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='brands'),
        ),
    ]
