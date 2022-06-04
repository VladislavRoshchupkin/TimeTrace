import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=50, verbose_name='Название отдела')),
                ('count_employee', models.IntegerField(default=0, verbose_name='Количество сотрудников')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'отделы',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_surname', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('employee_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('employee_patronymic', models.CharField(max_length=30, verbose_name='Отчество')),
                ('photo', models.ImageField(default='default.png', upload_to=app.models.Employee.upload, verbose_name='Фотография')),
                ('weekend_count', models.IntegerField(blank=True, default=0, verbose_name='Количество выходных')),
                ('department_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.department', verbose_name='К какому отделу относится')),
            ],
            options={
                'verbose_name': 'Сотрудника',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=30, verbose_name='Название должности')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=150, verbose_name='Название проекта')),
                ('project_description', models.TextField(max_length=250, verbose_name='Содержмое')),
                ('start_date', models.DateTimeField(verbose_name='Предполагаемое начало выполнения')),
                ('end_date', models.DateTimeField(verbose_name='Предполагаемый конец выполнения')),
                ('manager_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager_user_key', to='app.employee', verbose_name='К какому менеджеру')),
                ('project_user_key', models.ManyToManyField(related_name='project_key', to='app.Employee', verbose_name='К каким сотрудникам принадллежит проект')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=50, verbose_name='Название задачи')),
                ('task_description', models.TextField(max_length=250, verbose_name='Содержмое задачи')),
                ('start_date_task', models.DateTimeField(verbose_name='Предполагаемое начало выполнения')),
                ('end_date_task', models.DateTimeField(verbose_name='Предполагаемый конец выполнения')),
                ('status_task', models.CharField(choices=[('Сделано', 'Сделано'), ('В работе', 'В работе'), ('Не сделано', 'Не сделано')], max_length=50, verbose_name='Статус выполнения')),
                ('employee_key', models.ManyToManyField(related_name='employee_key', to='app.Employee', verbose_name='Какому сотруднику принадлежит задача')),
                ('task_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project', verbose_name='Какому проекту принадлежит задача')),
            ],
            options={
                'verbose_name': 'задачу',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='', max_length=100, verbose_name='Описание')),
                ('date_work', models.DateField(verbose_name='Выбранный день работы')),
                ('time_work', models.IntegerField(verbose_name='Проработанное количество часов')),
                ('task_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='app.task', verbose_name='К какой задаче принадлежит')),
                ('time_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employee', verbose_name='К какому сотруднику принадлежит')),
            ],
            options={
                'verbose_name': 'учет времени',
                'verbose_name_plural': 'учеты времени',
            },
        ),
        migrations.CreateModel(
            name='Raiting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_count', models.IntegerField(verbose_name='Общее количество наработанных часов в отделе')),
                ('raiting_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.department', verbose_name='К какому отделу относится рейтинг')),
            ],
            options={
                'verbose_name': 'рейтинг',
                'verbose_name_plural': 'рейтинги',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='position_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='app.position', verbose_name='Должность'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user_key',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='К какому User относится'),
        ),
    ]
