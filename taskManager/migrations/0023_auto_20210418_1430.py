# Generated by Django 3.1.2 on 2021-04-18 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0022_auto_20210418_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='time',
            field=models.DecimalField(blank=True, decimal_places=1, default=1.0, max_digits=3, null=True, verbose_name='所要時間(h)'),
        ),
    ]
