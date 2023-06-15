from django import forms
from .models import Product, UserProfile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'category']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'biography', 'location', 'avatar', 'website', 'date_of_birth', 'followers', 'address', 'phone_number']

