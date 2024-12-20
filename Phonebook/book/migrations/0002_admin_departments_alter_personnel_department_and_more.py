# Generated by Django 5.0.4 on 2024-11-02 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin_departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=200, verbose_name='Отдел')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделения',
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='personnel',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.departments', verbose_name='Отделение'),
        ),
        migrations.CreateModel(
            name='admin_personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_full_name', models.CharField(max_length=400, verbose_name='ФИО')),
                ('position', models.CharField(max_length=300, verbose_name='Должность')),
                ('phone', models.CharField(max_length=300, verbose_name='Телефон')),
                ('mail', models.CharField(max_length=300, verbose_name='Почта')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.admin_departments', verbose_name='Отдел')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
    ]
