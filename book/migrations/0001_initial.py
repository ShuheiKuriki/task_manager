# Generated by Django 3.0.2 on 2020-04-06 04:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='タイトル')),
                ('genre', models.CharField(blank=True, choices=[('小説', '小説'), ('アカデミック', 'アカデミック'), ('ビジネス', 'ビジネス'), ('自己啓発', '自己啓発')], max_length=32, null=True, verbose_name='ジャンル')),
                ('deadline', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='期限')),
                ('expired', models.BooleanField(default=False, verbose_name='期限切れ')),
                ('done_or_not', models.BooleanField(default=False)),
                ('done_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='完了した日')),
                ('order', models.IntegerField(default=0, verbose_name='順番')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
