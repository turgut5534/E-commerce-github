# Generated by Django 3.2.8 on 2021-12-25 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0053_alter_product_specs'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='is_cancelled',
            field=models.BooleanField(null=True),
        ),
    ]
