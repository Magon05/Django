from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator
import os


class product_category(models.Model):

    category_name = models.CharField(max_length=150, null=True, verbose_name='категория')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        managed = True

    def __str__(self):
        return self.category_name


class product_subcategory(models.Model):

    subcategory_name = models.CharField(max_length=150, null=True, verbose_name='подкатегория')
    category_name = models.ForeignKey(product_category, null=True, verbose_name="Категория", on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'подкатегории'
        managed = True

    def __str__(self):
        return self.subcategory_name


class goods(models.Model):

    product_name = models.CharField(max_length=300, blank=True, verbose_name='название продукта')
    regular_price = models.IntegerField(verbose_name='обычная цена')
    discounted_price = models.IntegerField(blank=True, verbose_name='скидочная цена')
    stock_quantity = models.IntegerField(verbose_name='количество товара')
    product_details = models.CharField(blank=True, verbose_name='описание продукта')
    category = models.ForeignKey(product_category, null=True, verbose_name='категория', on_delete=models.SET_NULL)
    sub_category = models.ForeignKey(product_subcategory, null=True, verbose_name='подкатегория', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='дата создания')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class product_image(models.Model):
    product = models.ForeignKey(goods, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])


class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=300, blank=True, verbose_name='название продукта')
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    product = models.ForeignKey(goods, related_name='cart_product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    def get_absolute_url(self):
        return reverse("cart_detail")
