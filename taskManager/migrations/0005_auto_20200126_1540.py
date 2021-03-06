# Generated by Django 3.0.2 on 2020-01-26 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0004_auto_20200126_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='important',
            field=models.BooleanField(choices=[(True, '○'), (False, '✖️')], default=True, verbose_name='重要'),
        ),
        migrations.AlterField(
            model_name='task',
            name='urgent',
            field=models.BooleanField(choices=[(True, '○'), (False, '✖️')], default=True, verbose_name='緊急'),
        ),
    ]
