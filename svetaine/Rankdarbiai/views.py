from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, UserProfile, Review, Favorite, Cart, CartItem, Transaction, PromoCode
from .forms import ProductForm, UserProfileForm, UserForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def home(request):
    categories = Category.objects.all()
    latest_products = Product.objects.all().order_by('-created_at')[:5]
    context = {
        'categories': categories,
        'latest_products': latest_products
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.password = make_password(user_form.cleaned_data['password'], hasher='pbkdf2_sha256')
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()


            return redirect('registration_success')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

def registration_success(request):
    return render(request, 'registration_success.html')

def save_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.profile = UserProfile(user=instance)
        instance.profile.save()

@login_required
def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_products = user_profile.user_products.all()
    context = {
        'user_profile': user_profile,
        'user_products': user_products
    }
    return render(request, 'user_profile.html', context)


@login_required
def edit_profile(request):
    user = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            request.user.userprofile.user_products.add(product)
            return redirect('user_profile')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.product = product
            new_review.user = request.user
            new_review.save()
    else:
        form = ReviewForm()
    context = {
        'product': product,
        'reviews': reviews,
        'form': form
    }
    return render(request, 'product_detail.html', context)

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'delete_product.html', {'product': product})

@login_required
def confirm_delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('user_profile')


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

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'favorites.html', {'favorites': favorites})

@login_required
def add_to_favorites(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=user, product=product)

    if created:
        messages.success(request, f'Produktas "{product.title}" buvo pridėtas prie mėgstamiausių.')
    else:
        messages.info(request, f'Produktas "{product.title}" jau yra jūsų mėgstamųjų sąraše.')

    return redirect('products')

@login_required
def remove_from_favorites(request, product_id):
    Favorite.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('favorites')


@login_required
def cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total_price = sum([item.product.price * item.quantity for item in cart_items])
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()

    if created:
        messages.success(request, f'Produktas "{product.title}" buvo įdėtas į krepšelį.')
    else:
        messages.info(request, f'Produktas "{product.title}" jau yra įdėtas į krepšelį.')

    return redirect('products')

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        user_cart = Cart.objects.get(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(cart=user_cart, product=product)
        quantity = request.POST.get('quantity')
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart')

@login_required
def apply_promo_code(request):
    promo_code = request.POST.get('promo_code')
    promo = PromoCode.objects.filter(code=promo_code).first()
    if promo and promo.is_valid():
        request.session['promo_code'] = promo.code
        messages.success(request, 'Nuolaidos kodas sėkmingai pritaikytas!')
    elif promo and not promo.is_valid():
        messages.error(request, 'Jūsų nuolaidos kodas nebegalioja.')
    else:
        messages.error(request, 'Jūsų nuolaidos kodas nerastas.')
    return redirect('checkout')



@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')

@login_required
def process_payment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        card_holder = request.POST.get('card_holder')
        card_number = request.POST.get('card_number')
        expiration = request.POST.get('expiration')
        cvv = request.POST.get('cvv')

        if name and email and address and city and state and card_holder and card_number and expiration and cvv:
            return redirect('payment_success')
        else:
            return redirect('payment_failure')
    else:
        return redirect('checkout')


@login_required
def checkout(request):
    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total_price = sum([item.product.price * item.quantity for item in cart_items])
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    if request.method == 'POST':
        card_number = request.POST.get('cc-number')
        card_holder = request.POST.get('cc-name')
        payment_success = process_payment(total_price, card_number, card_holder)

        if payment_success:
            cart_items.delete()
            return redirect('payment_success')
        else:
            return redirect('payment_failure')

    return render(request, 'checkout.html', context)


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

def help(request):
    return render(request, 'help.html')

