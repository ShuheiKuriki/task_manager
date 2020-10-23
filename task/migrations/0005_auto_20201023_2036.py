# Generated by Django 3.1.2 on 2020-10-23 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20201023_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='days',
            field=models.IntegerField(choices=[(0, '毎日'), (1, '月'), (2, '火'), (3, '水'), (4, '木'), (5, '金'), (6, '土'), (7, '日')], default=0, verbose_name='曜日タイプ'),
        ),
    ]