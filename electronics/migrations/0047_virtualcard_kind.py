# Generated by Django 3.2.8 on 2021-11-28 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0046_payment_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualcard',
            name='kind',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
