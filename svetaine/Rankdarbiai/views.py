from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, UserProfile, Review, Favorite, Cart, CartItem, Transaction
import stripe
from django.http import HttpResponse

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
        message = 'Продукт успешно добавлен в избранное'
    else:
        message = 'Продукт уже есть в избранном'
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


stripe.api_key = 'fasfasfasfssdffčęčęč'


def payment(request):
    if request.method == 'POST':
        stripe_token = request.POST.get('stripeToken')  # Gaukime Stripe Token iš POST duomenų
        card_number = request.POST.get('card_number')
        card_holder = request.POST.get('card_holder')

        # Čia vykdykite mokėjimo logiką su gautais duomenimis
        # Pavyzdžiui, siųskite mokėjimo užklausą į Stripe API

        # Jei mokėjimas sėkmingas, grąžinkime atsakymą
        return HttpResponse('Mokėjimas sėkmingas!')

    return render(request, 'payment.html')

def process_payment(request):
    stripe.api_key = 'fasfasfasfssdffčęčęč'

    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        card_number = request.POST.get('card_number')
        card_holder = request.POST.get('card_holder')

        # Čia įvykdykite mokėjimo veiksmus su Stripe

        # Jei mokėjimas sėkmingas, grąžinkite "payment_success.html" šabloną
        return render(request, 'payment_success.html')

    # Jei užklausa nėra POST, grąžinkite "payment.html" šabloną
    return render(request, 'payment.html')