# Generated by Django 4.0.3 on 2022-04-03 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_time_task_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False, verbose_name='Статус выполненной задачи'),
        ),
        migrations.AlterField(
            model_name='time',
            name='task_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='app.task', verbose_name='К какой задаче принадлежит'),
        ),
    ]