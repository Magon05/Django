from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegister(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control'}))

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("Пользователь с таким именем уже существует")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email уже занят")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2


class CreateForm(forms.Form):
    #product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'control mb-4'}))

    class Meta:
        model = goods
        fields = "__all__" #('product_name', 'regular_price', 'discounted_price', 'stock_quantity', 'product_details', 'category')
        widgets = {
            "product_name": forms.Textarea(attrs={'class': 'form-control mb-4'}),
        }

        """def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['product_name'].widget.attrs.update({'class': 'control mb-4'})

        field_classes = {
                    "product_name": forms.TextInput(attrs={'class': 'form-control mb-4'}),
                }"""