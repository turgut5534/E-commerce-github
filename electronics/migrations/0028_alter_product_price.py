# Generated by Django 3.2.8 on 2021-11-25 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0027_alter_orderdetail_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
    ]
