
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

        DEPARTMENT_CHOICES = (
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('surgery', 'Surgery'),
       
         )
        
        user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
        department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, blank=True, null=True)
        full_name = models.CharField(max_length=100, blank=True, null=True)
        cv = models.FileField(upload_to='cvs/', blank=False, null=True) 
        mobile_number = models.CharField(max_length=15, blank=True, null=True)
        qualification = models.CharField(blank=True, null=True)
        profile_pic = models.ImageField(upload_to='profile_pics/doctors/', blank=True, null=True)
        address = models.CharField(blank=True, null=True)
        is_approved = models.BooleanField(default=False)


        def __str__(self):
             return self.user.get_full_name()
        
        def save(self, *args, **kwargs):
            if self.qualification:
                 self.qualification = self.qualification.upper()
            super(Doctor, self).save(*args, **kwargs)

        


    
    


class Patient(models.Model):
     
     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
     full_name = models.CharField(max_length=50,blank=True, null=True) 
     mobile_number = models.CharField(max_length=15, blank=True, null=True)
     profile_pic = models.ImageField(upload_to='profile_pics/patients/', blank=True, null=True)
     address = models.CharField(blank=True, null=True) 



class TimeSlot(models.Model):
    

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    booked = models.BooleanField(default=False) 


    def __str__(self):
        return f'{self.doctor.user.get_full_name()} - {self.start_time} to {self.end_time} on {self.date}'
    
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True) 
    prescription = models.FileField(upload_to='prescriptions/', blank=True, null=True)
    patient_age = models.PositiveIntegerField(default=0)
    describe_problem = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"Appointment {self.pk} - {self.patient.full_name} with {self.doctor.full_name}"