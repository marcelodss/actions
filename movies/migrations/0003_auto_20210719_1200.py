# Generated by Django 3.2.4 on 2021-07-19 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20210719_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='data',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='usuario',
        ),
    ]
