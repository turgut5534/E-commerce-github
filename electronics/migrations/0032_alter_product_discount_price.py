# Generated by Django 3.2.8 on 2021-11-26 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0031_alter_wishlist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]