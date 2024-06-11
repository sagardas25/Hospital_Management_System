from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . import models
from .models import CustomUser , TimeSlot
from django.contrib.auth import get_user_model
User = get_user_model()
import datetime



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




class TimeSlotForm(forms.Form):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    ]

    TIME_SLOTS = [
        ('10:00-13:00', '10:00 AM - 1:00 PM'),
        ('13:00-16:00', '1:00 PM - 4:00 PM'),
        ('16:00-19:00', '4:00 PM - 7:00 PM'),
        ('19:00-22:00', '7:00 PM - 10:00 PM')
    ]

    day = forms.ChoiceField(choices=DAYS_OF_WEEK)
    time_slots = forms.MultipleChoiceField(choices=TIME_SLOTS, widget=forms.CheckboxSelectMultiple)


