"""
URL configuration for minishop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from magazine import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:cart_item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('category_list/delete_category/<slug:pk>/', views.Delete_category.as_view(), name='delete_category'),
    path('subcategory_list/delete_subcategory/<slug:pk>/', views.Delete_subcategory.as_view(), name='delete_subcategory'),
    path("edit/<slug:pk>/", views.edit_product, name="edit"),
    path("delete/<slug:pk>/", views.Delete.as_view(), name="delete"),
    path("create/", views.create, name='create'),
    path("create_category/", views.create_category, name='create_category'),
    path("create_subcategory/", views.create_subcategory, name='create_subcategory'),
    path('product_info/', views.Product_info.as_view()),
    path('login/', views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path('register/', views.Register.as_view(), name="register"),
    path("test/", views.test, name="test"),
    path("cart/", views.cart_detail, name="cart"),
    path("account/", views.Account.as_view(), name="account"),
    path('category_list/', views.Category_list.as_view(), name='category_list'),
    path('subcategory_list/', views.Subcategory_list.as_view(), name='subcategory_list'),
    path('admin/', admin.site.urls),
    path('', views.Main.as_view(), name="main"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)