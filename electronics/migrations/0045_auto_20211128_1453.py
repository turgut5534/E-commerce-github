# Generated by Django 3.2.8 on 2021-11-28 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0044_delete_orderitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentDetail',
        ),
        migrations.DeleteModel(
            name='UserPayment',
        ),
    ]
