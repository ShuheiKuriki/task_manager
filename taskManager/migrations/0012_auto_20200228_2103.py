# Generated by Django 3.0.2 on 2020-02-28 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0011_auto_20200210_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='important',
            field=models.BooleanField(verbose_name='重要'),
        ),
    ]
