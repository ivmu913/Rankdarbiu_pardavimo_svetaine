from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, UserProfile, Review, Favorite, Cart, CartItem, Transaction
from django.http import HttpResponse
from .forms import ProductForm

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    return render(request, 'register.html')

def products(request):
    return render(request, 'products.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def category_products(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'category_products.html', context)

def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'product_detail.html', context)


@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        total_price = product.price * quantity
        order = Order.objects.create(product=product, buyer=request.user, quantity=quantity, total_price=total_price)
        return render(request, 'order_confirmation.html', {'order': order})
    else:
        return render(request, 'create_order.html', {'product': product})


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if created:
        message = 'Prekė sėkmingai pridėta į mėgstamiausius'
    else:
        message = 'Prekė jau yra jūsų mėgstamiausių sąraše'
    return render(request, 'add_to_favorites.html', {'message': message})


@login_required
def cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.products.all()
    context = {
        'cart_items': cart_items
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=user_cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    user_cart = Cart.objects.get(user=request.user)
    cart_items = user_cart.products.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    transaction = Transaction.objects.create(buyer=request.user, total_price=total_price)
    user_cart.products.clear()
    return render(request, 'checkout.html', {'transaction': transaction})


@login_required
def user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'user_profile.html', context)


@login_required
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        return redirect('user_profile')
    else:
        context = {
            'user_profile': user_profile
        }
        return render(request, 'edit_profile.html', context)


def fake_payment(request):
    if request.method == 'POST':
        payment_amount = request.POST.get('amount')
        card_number = request.POST.get('card_number')
        card_holder = request.POST.get('card_holder')

        payment_success = True

        if payment_success:
            return render(request, 'payment_success.html')
        else:
            return render(request, 'payment_failure.html')

    return render(request, 'fake_payment.html')


def payment_success(request):
    return render(request, 'payment_success.html')


def payment_failure(request):
    return render(request, 'payment_failure.html')
