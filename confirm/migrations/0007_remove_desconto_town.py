# Generated by Django 3.2.4 on 2021-10-07 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confirm', '0006_auto_20211007_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='desconto',
            name='town',
        ),
    ]
