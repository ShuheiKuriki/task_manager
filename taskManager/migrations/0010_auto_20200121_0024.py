# Generated by Django 3.0.2 on 2020-01-20 15:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0009_auto_20200120_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 21), null=True, verbose_name='期限'),
        ),
        migrations.AlterField(
            model_name='task',
            name='when',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 21), verbose_name='実行予定日'),
        ),
    ]
