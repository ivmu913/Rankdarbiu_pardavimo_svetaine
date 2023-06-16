from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, UserProfile, Review, Favorite, Cart, CartItem, Transaction, PromoCode
from .forms import ProductForm, UserProfileForm, UserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


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


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                return redirect('register')
            else:
                # Use create_user method to encrypt password
                user = User.objects.create_user(username=username, email=email, password=password)

                # Create a user profile for the new user
                profile = UserProfile(user=user)
                profile.save()

                messages.success(request, f'Vartotojas {username} sėkmingai užregistruotas!')
                return redirect('registration_success')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')

    return render(request, 'register.html')


def registration_success(request):
    return render(request, 'registration_success.html')

@login_required
def user_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_products = user_profile.user_products.all()  # Gauti įdėtas prekes
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
            request.user.userprofile.user_products.add(product)  # Įdedama prekė į vartotojo profilio prekių sąrašą
            return redirect('user_profile')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

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

    # pridėti pranešimą
    # messages.success(request, "Jūsų prekė sėkmingai pridėta į krepšelį.")
    # po to, kai prekė pridėta į krepšelį, nukreipia atgal į prekių sąrašą
    return redirect('products')
    # nukreipia atgal į puslapį, iš kurio vartotojas atėjo
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
    cart = Cart.objects.get(user=request.user)  # Gaukite vartotojo krepšelį
    product = get_object_or_404(Product, id=product_id)  # Raskite produktą pagal ID
    cart_item = CartItem.objects.get(cart=cart, product=product)  # Raskite prekę krepšelyje
    cart_item.delete()  # Pašalinkite prekę iš krepšelio
    return redirect('cart')  # Grįžkite į krepšelio puslapį




@login_required
def checkout(request):
    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    total_price = sum([item.product.price * item.quantity for item in cart_items])
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
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
