# Generated by Django 3.1.2 on 2021-04-18 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0021_auto_20200819_0632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='important',
        ),
        migrations.RemoveField(
            model_name='task',
            name='urgent',
        ),
        migrations.AddField(
            model_name='task',
            name='fixed',
            field=models.BooleanField(default=False, verbose_name='予定'),
        ),
        migrations.AddField(
            model_name='task',
            name='time',
            field=models.DecimalField(blank=True, decimal_places=1, default=1.0, max_digits=3, null=True, verbose_name='所要時間'),
        ),
    ]