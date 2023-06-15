from django import forms
from .models import Product, UserProfile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'category']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['biography', 'location', 'avatar', 'website', 'date_of_birth']
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        }