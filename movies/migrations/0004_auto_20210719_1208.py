# Generated by Django 3.2.4 on 2021-07-19 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import movies.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0003_auto_20210719_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='data',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='alguma data '),
        ),
        migrations.AddField(
            model_name='genre',
            name='newscore',
            field=models.IntegerField(default=0, validators=[movies.models.validate_score], verbose_name='Score'),
        ),
        migrations.AddField(
            model_name='genre',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='set_usuario', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
