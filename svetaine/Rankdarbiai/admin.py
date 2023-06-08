from django.contrib import admin
from .models import Category, Product, Order, UserProfile, Review, Favorite, Cart, CartItem, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at', 'owner')
    list_filter = ('category', 'created_at', 'owner')
    search_fields = ('title', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'buyer', 'quantity', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__title', 'buyer__username')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created_at')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'total_price', 'created_at')



