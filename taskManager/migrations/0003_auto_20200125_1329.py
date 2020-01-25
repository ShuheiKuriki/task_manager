# Generated by Django 3.0.2 on 2020-01-25 04:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0002_auto_20200124_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 25), null=True, verbose_name='期限'),
        ),
        migrations.AlterField(
            model_name='task',
            name='done_date',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 25), null=True, verbose_name='完了した日'),
        ),
        migrations.AlterField(
            model_name='task',
            name='when',
            field=models.DateField(blank=True, default=datetime.date(2020, 1, 25), verbose_name='実行予定日'),
        ),
    ]
