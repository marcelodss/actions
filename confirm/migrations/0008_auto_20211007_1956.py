# Generated by Django 3.2.4 on 2021-10-07 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('confirm', '0007_remove_desconto_town'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemsale',
            name='desconto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='confirm.desconto'),
        ),
        migrations.AlterField(
            model_name='shoppingmall',
            name='town',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='confirm.town'),
        ),
    ]
