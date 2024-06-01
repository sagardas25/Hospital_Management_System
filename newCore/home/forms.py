from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . import models
from .models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()



class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('doctor','doctor'),
        ('patient','patient'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User 
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None  

