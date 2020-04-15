from django.forms import ModelForm
from .models import Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class Orderform(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreatUserForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['username','email','password1','password2']