# Generated by Django 3.2.8 on 2021-11-25 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0021_auto_20211125_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='electronics.address'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='electronics.payment'),
        ),
    ]
