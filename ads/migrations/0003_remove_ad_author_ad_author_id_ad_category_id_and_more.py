# Generated by Django 4.2.1 on 2023-05-16 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='author',
        ),
        migrations.AddField(
            model_name='ad',
            name='author_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ads.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='category_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ads.category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='image',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
