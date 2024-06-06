
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('doctor','doctor'),
        ('patient','patient'),
    )
    
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True, verbose_name='groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True, verbose_name='user permissions')




class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.get_full_name()
    
    


class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.doctor.user.get_full_name()} - {self.start_time} to {self.end_time} on {self.date}'


