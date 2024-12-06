from django.db import models


class personal_data(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')