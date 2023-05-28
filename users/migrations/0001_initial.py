# Generated by Django 4.2.1 on 2023-05-28 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=8, null=True)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=8, null=True)),
            ],
            options={
                'verbose_name': 'Название',
                'verbose_name_plural': 'Названия',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40, null=True)),
                ('last_name', models.CharField(max_length=40, null=True)),
                ('username', models.CharField(max_length=40, null=True, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('role', models.CharField(choices=[('member', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='member', max_length=40)),
                ('age', models.SmallIntegerField(null=True)),
                ('location', models.ManyToManyField(to='users.location')),
            ],
            options={
                'verbose_name': 'Имя пользователя',
                'verbose_name_plural': 'Имена пользователей',
            },
        ),
    ]