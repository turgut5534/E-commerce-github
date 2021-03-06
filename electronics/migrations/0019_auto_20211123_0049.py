# Generated by Django 3.2.8 on 2021-11-22 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0018_auto_20211106_0643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='modified_at',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='electronics.address'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order_code',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
