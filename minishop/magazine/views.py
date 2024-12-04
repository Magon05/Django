from .models import *
from django.views.generic import ListView, FormView, DeleteView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files import File
from django.db.models.signals import post_delete
from django.db.models import Sum
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.core.paginator import Paginator



#------------------------------------------Главная--------------------------------------
class Main(ListView):

    model = goods
    template_name = 'shop.html'
    context_object_name = 'goods'
    paginate_by = 4


    def get_queryset(self):
        get_search = self.request.GET.get("search")
        get_category = self.request.GET.get("category")
        get_subcategory = self.request.GET.get("subcategory")
        get_ordering = self.request.GET.get('orderby', 'product_name')
        if get_search:
            queryset = goods.objects.filter(product_name__icontains=get_search).order_by(get_ordering)
        elif get_category and get_subcategory:
            queryset = goods.objects.filter(category=get_category, sub_category=get_subcategory).order_by(get_ordering)
        elif get_category:
            queryset = goods.objects.filter(category=get_category).order_by(get_ordering)
        else:
            queryset = goods.objects.order_by(get_ordering)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = {}

        for i in goods.objects.values('id'):
            images[i['id']] = ["".join(u) for u in product_image.objects.filter(product=i['id']).values_list('image')]

        context['images'] = images
        context['category_list'] = product_category.objects.values_list('id', 'category_name')
        context['subcategories_list'] = product_subcategory.objects.values_list('id', 'subcategory_name', 'category_name')
        if self.request.user.is_authenticated == True:
            context['cart_items_counts'] = cart.objects.filter(user=self.request.user).aggregate(total=Sum('quantity'))['total']
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


class Product_info(ListView):

    model = goods
    template_name = 'shopdes.html'
    context_object_name = 'goods'

    def get_queryset(self):
        param = self.request.GET.get('id')
        queryset = goods.objects.filter(id=param)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = goods.objects.get(id=self.request.GET.get('id'))
        images = ["".join(u) for u in product_image.objects.filter(product=product.id).values_list('image')]
        context['images'] = images
        context['category'] = product_category.objects.get(id=product.category_id)
        context['subcategory'] = product_subcategory.objects.get(id=product.sub_category_id)
        context['cart_items_counts'] = cart.objects.filter(user=self.request.user).aggregate(total=Sum('quantity'))['total']
        return context


class Create_product(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = goods
    fields = '__all__'
    permission_required = 'magazine.add_goods'
    success_url = reverse_lazy('main')
    template_name = "create_and_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = product_category.objects.values('id', 'category_name')
        context['sub_categories'] = {i['id']: list(product_subcategory.objects.filter(category_name=i['id']).values('id', 'subcategory_name')) for i in context['categories']}
        context['cart_items_counts'] = cart.objects.filter(user=self.request.user).aggregate(total=Sum('quantity'))['total']
        context['current_operation'] = 'Добавление товара'
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        product.category = product_category.objects.get(id=self.request.POST.get("category"))
        product.sub_category = product_subcategory.objects.get(id=self.request.POST.get("sub_category"))
        product.save()

        images = self.request.FILES.getlist('images', default=None)
        if images:
            for image in images:
                product_image.objects.create(product=product, image=image)

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['status'] = "Ошибка! Вы не заполнили все поля или ввели неправильные данные!"
        return self.render_to_response(context)

    def handle_no_permission(self):
        return super().handle_no_permission()


class Edit_product(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = goods
    fields = '__all__'
    permission_required = 'magazine.change_goods'
    success_url = reverse_lazy('main')
    template_name = "create_and_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = product_category.objects.values('id', 'category_name')
        context['sub_categories'] = {i['id']: list(product_subcategory.objects.filter(category_name=i['id']).values('id', 'subcategory_name')) for i in context['categories']}
        context['cart_items_counts'] = cart.objects.filter(user=self.request.user).aggregate(total=Sum('quantity'))['total']
        context['editable_stuff'] = goods.objects.get(id=self.kwargs.get('pk'))
        context['current_operation'] = 'Изменение товара'
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        product.category = product_category.objects.get(id=self.request.POST.get("category"))
        product.sub_category = product_subcategory.objects.get(id=self.request.POST.get("sub_category"))
        product.save()

        images = self.request.FILES.getlist('images', default=None)
        if images:
            for image in images:
                product_image.objects.create(product=product, image=image)

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['status'] = "Ошибка! Вы не заполнили все поля или ввели неправильные данные!"
        return self.render_to_response(context)

    def handle_no_permission(self):
        return super().handle_no_permission()


class Delete_product(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = goods
    success_url = reverse_lazy('main')
    permission_required = 'magazine.delete_goods'

    def handle_no_permission(self):
        return super().handle_no_permission()


@receiver(post_delete, sender=product_image)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
#------------------------------------------/Главная--------------------------------------


#------------------------------------------Категории--------------------------------------
class Category_list(ListView, LoginRequiredMixin, PermissionRequiredMixin,):

    model = product_category
    context_object_name = "data"
    template_name = 'category_list.html'
    permission_required = 'magazine.view_product_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items_counts'] = cart.objects.filter(user=self.request.user).aggregate(total=Sum('quantity'))['total']
        return context

    def handle_no_permission(self):
        return super().handle_no_permission()


class Delete_category(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = product_category
    success_url = reverse_lazy('category_list')
    permission_required = 'magazine.delete_product_category'

    def handle_no_permission(self):
        return super().handle_no_permission()


@login_required
@permission_required('magazine.add_product_category', raise_exception=True)
def create_category(request):
    category_name = request.POST.get("category_name")
    if category_name:
        category = product_category(category_name=category_name)
        category.save()
        return redirect('category_list')
    else:
        return redirect('category_list')


class Subcategory_list(ListView, LoginRequiredMixin, PermissionRequiredMixin):

    model = product_subcategory
    context_object_name = "data"
    template_name = 'subcategory_list.html'
    permission_required = 'magazine.view_product_subcategory'

    def handle_no_permission(self):
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = product_category.objects.values('id', 'category_name')
        context['cart_items_counts'] = cart.objects.filter(user=self.request.user).aggregate(total=Sum('quantity'))['total']
        return context


class Delete_subcategory(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = product_subcategory
    success_url = reverse_lazy('subcategory_list')
    permission_required = 'magazine.delete_product_subcategory'

    def handle_no_permission(self):
        return super().handle_no_permission()


@login_required
@permission_required('magazine.add_product_subcategory', raise_exception=True)
def create_subcategory(request):
    subcategory_name = request.POST.get("subcategory_name")
    category = product_category.objects.get(id=int(request.POST.get("category")))
    if subcategory_name:
        subcategory = product_subcategory(subcategory_name=subcategory_name, category_name=category)
        subcategory.save()
        return redirect('subcategory_list')
    else:
        return redirect('subcategory_list')

#------------------------------------------/Категории--------------------------------------


#------------------------------------------Корзина--------------------------------------
@login_required
def add_to_cart(request, product_id):
    cart_item = cart.objects.filter(user=request.user, product_id=product_id).first()
    product = goods.objects.get(id=product_id)
    if cart_item:
        cart_item.quantity += 1
        cart_item.total_price += product.discounted_price
        cart_item.save()
    else:
        cart.objects.create(user=request.user, product_id=product.id, price=product.discounted_price, total_price=product.discounted_price, product_name=product.product_name)

    return redirect("main")


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(cart, id=cart_item_id)

    if cart_item.user == request.user:
        cart_item.delete()

    return redirect("cart")


@login_required
def cart_detail(request):
    images = {}
    cart_items = cart.objects.filter(user=request.user)
    cart_items_counts = cart.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total']
    cart_items_total_price = cart.objects.filter(user=request.user).aggregate(total=Sum('total_price'))['total']
    product_id_list = [i.product_id for i in cart_items]
    for i in product_id_list: #goods.objects.values('id'):
        images[i] = ["".join(u) for u in product_image.objects.filter(product=i).values_list('image')]

    context = {
        "cart_items": cart_items,
        'cart_items_counts': cart_items_counts,
        'cart_items_total_price': cart_items_total_price,
        "product_id_list": product_id_list,
        "images": images,
    }
    return render(request, "cart.html", context)
#------------------------------------------/Корзина--------------------------------------


#------------------------------------------Аккаунт--------------------------------------
class Account(ListView):
    model = goods
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items_counts'] = cart.objects.filter(user=self.request.user).aggregate(total=Sum('quantity'))['total']
        return context

class Login(LoginView):

    form_class = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('main')


class Logout(LogoutView):

    next_page = "main"


class Register(FormView):

    form_class = UserRegister
    success_url = reverse_lazy('main')
    template_name = "register.html"

    def form_valid(self, form):
        user = form.save()
        buyers_group = Group.objects.get(name='buyers')
        user.groups.add(buyers_group)
        login(self.request, user)
        return super(Register, self).form_valid(form)

#------------------------------------------/Аккаунт--------------------------------------