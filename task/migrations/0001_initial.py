# Generated by Django 3.1.2 on 2020-10-23 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, verbose_name='タスク名')),
                ('important', models.BooleanField(default=False, verbose_name='重要')),
                ('urgent', models.BooleanField(default=False, verbose_name='緊急')),
                ('period', models.IntegerField(choices=[(0, '~12時'), (1, '12~15時'), (2, '15~18時'), (3, '18~21時'), (4, '21時~')], default=0, verbose_name='時間帯')),
                ('days', models.IntegerField(choices=[(0, '毎日'), (1, '平日'), (2, '週末'), (3, '月'), (4, '火'), (5, '水'), (6, '木'), (7, '金'), (8, '土'), (9, '日')], default=0, verbose_name='曜日')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]