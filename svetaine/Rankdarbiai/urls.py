from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('add_product/', views.add_product, name='add_product'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/delete/confirm/<int:product_id>/', views.confirm_delete_product, name='confirm_delete_product'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('categories/', views.all_categories, name='categories'),
    path('payment/', views.fake_payment, name='fake_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('order/create/<int:product_id>/', views.create_order, name='create_order'),
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('apply_promo_code/', views.apply_promo_code, name='apply_promo_code'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('help/', views.help, name='help'),
]

