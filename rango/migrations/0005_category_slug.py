# Generated by Django 2.1.5 on 2021-09-13 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_auto_20210913_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
