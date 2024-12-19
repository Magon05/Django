# Generated by Django 5.0.4 on 2024-12-17 14:38

import django.db.models.deletion
import main.utilities
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rubric_subrubric_superrubric_rubric_super_rubric'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='Товар')),
                ('content', models.TextField(verbose_name='Описание')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('contacts', models.TextField(verbose_name='Контакты')),
                ('image', models.ImageField(blank=True, upload_to=main.utilities.get_timestamp_path, verbose_name='Изображение')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Выводить в списке?')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор объявления')),
                ('rubric', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.subrubric', verbose_name='Рубрика')),
            ],
            options={
                'verbose_name': 'Объявления',
                'verbose_name_plural': 'Объявления',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=main.utilities.get_timestamp_path, verbose_name='Изображение')),
                ('bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bb', verbose_name='Объявления')),
            ],
            options={
                'verbose_name': 'Дополнительная иллюстрация',
                'verbose_name_plural': 'Дополнительные иллюстрации',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=30, verbose_name='Автор')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Выводить на экран?')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликован')),
                ('bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bb', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Комментарии',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['created_at'],
            },
        ),
    ]