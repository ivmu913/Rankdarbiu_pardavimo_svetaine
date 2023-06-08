from django.urls import path
from . import views
from .views import process_payment

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('products/', views.products, name='products'),
    path('payment/', views.payment, name='payment'),
    path('process_payment/', process_payment, name='process_payment'),
    # path('process_payment/', views.process_payment, name='process_payment'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('order/create/<int:product_id>/', views.create_order, name='create_order'),
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
