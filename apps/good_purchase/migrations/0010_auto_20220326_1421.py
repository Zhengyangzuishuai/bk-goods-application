# Generated by Django 2.2.6 on 2022-03-26 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('good_purchase', '0009_auto_20220326_0144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='create_user',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='update_user',
        ),
        migrations.RemoveField(
            model_name='good',
            name='create_user',
        ),
        migrations.RemoveField(
            model_name='good',
            name='update_user',
        ),
        migrations.RemoveField(
            model_name='groupapply',
            name='create_user',
        ),
        migrations.RemoveField(
            model_name='groupapply',
            name='update_user',
        ),
        migrations.RemoveField(
            model_name='withdraw',
            name='create_user',
        ),
        migrations.RemoveField(
            model_name='withdraw',
            name='update_user',
        ),
    ]
