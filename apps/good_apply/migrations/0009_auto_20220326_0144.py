# Generated by Django 2.2.6 on 2022-03-26 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('good_apply', '0008_auto_20220227_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='create_user',
            field=models.CharField(default='admin', max_length=120, verbose_name='创建用户'),
        ),
        migrations.AddField(
            model_name='apply',
            name='update_user',
            field=models.CharField(default='admin', max_length=120, verbose_name='更新用户'),
        ),
        migrations.AddField(
            model_name='review',
            name='create_user',
            field=models.CharField(default='admin', max_length=120, verbose_name='创建用户'),
        ),
        migrations.AddField(
            model_name='review',
            name='update_user',
            field=models.CharField(default='admin', max_length=120, verbose_name='更新用户'),
        ),
    ]
