# Generated by Django 3.2.4 on 2022-06-20 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confirm', '0008_auto_20211007_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, unique=True),
        ),
    ]
