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
    path("edit_product/<slug:pk>/", views.Edit_product.as_view(), name="edit_product"),
    path("delete_product/<slug:pk>/", views.Delete_product.as_view(), name="delete_product"),
    path("create_product/", views.Create_product.as_view(), name='create_product'),
    path("create_category/", views.create_category, name='create_category'),
    path("create_subcategory/", views.create_subcategory, name='create_subcategory'),
    path('product_info/', views.Product_info.as_view()),
    path('login/', views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path('register/', views.Register.as_view(), name="register"),
    path("cart/", views.cart_detail, name="cart"),
    path("account/", views.Account.as_view(), name="account"),
    path('category_list/', views.Category_list.as_view(), name='category_list'),
    path('subcategory_list/', views.Subcategory_list.as_view(), name='subcategory_list'),
    path('admin/', admin.site.urls),
    path('', views.Main.as_view(), name="main"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)