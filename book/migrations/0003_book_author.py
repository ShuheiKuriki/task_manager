# Generated by Django 3.0.2 on 2020-04-07 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20200407_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='著者'),
        ),
    ]
