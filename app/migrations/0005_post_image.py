# Generated by Django 2.2.12 on 2020-07-09 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200707_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='イメージ画像'),
        ),
    ]