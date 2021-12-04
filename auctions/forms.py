from django.forms import ModelForm, TextInput
from .models import Auction, User
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['user', 'category', 'title', 'image', 'description', 'starting_price', 'date', 'active']