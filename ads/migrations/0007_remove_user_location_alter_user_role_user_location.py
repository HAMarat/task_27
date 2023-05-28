# Generated by Django 4.2.1 on 2023-05-22 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0006_rename_author_id_ad_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='location',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('member', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='member', max_length=40),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.ManyToManyField(null=True, to='ads.location'),
        ),
    ]
