# Generated by Django 3.2.9 on 2022-04-16 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_task_completed_alter_time_task_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='time',
            name='description',
            field=models.TextField(default='', max_length=100, verbose_name='Описание'),
        ),
    ]
