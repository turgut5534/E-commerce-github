# Generated by Django 3.2.8 on 2021-11-26 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('electronics', '0034_rename_category_marka_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
    ]
