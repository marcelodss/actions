# Generated by Django 3.2.4 on 2021-10-07 20:26

import confirm.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('confirm', '0004_auto_20210924_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('headshot', models.ImageField(blank=True, null=True, upload_to='tmp/gm/headshots')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_created=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('currency', models.CharField(choices=[('CAD', 'CAD'), ('USD', 'USD')], max_length=3)),
                ('date', models.DateField()),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confirm.shop')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingMall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('general_manager', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='confirm.generalmanager')),
                ('shops', models.ManyToManyField(blank=True, to='confirm.Shop')),
                ('town', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='confirm.town')),
            ],
        ),
        migrations.CreateModel(
            name='ItemSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('currency', models.CharField(max_length=5, validators=[confirm.validators.validate_currency])),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='confirm.item')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_sales', to='confirm.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('confirm.transaction',),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('notes', models.TextField(blank=True, default='This is the default', null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confirm.item')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='confirm.shop')),
            ],
            options={
                'verbose_name_plural': 'Inventory',
                'ordering': ['shop', 'item__name'],
                'unique_together': {('shop', 'item')},
            },
        ),
    ]
