# Generated by Django 3.0.2 on 2020-06-24 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0020_auto_20200425_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='done_date',
            field=models.DateField(blank=True, default='', null=True, verbose_name='完了した日'),
        ),
    ]
