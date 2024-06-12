from django.contrib import admin
from .models import CustomUser
from .models import Doctor


# Register your models here.

class customUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser,customUserAdmin) 



class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'full_name', 'mobile_number', 'address']
    search_fields = ['user__username', 'full_name', 'department']
    list_filter = ['department']
    fields = ['user', 'department', 'full_name', 'mobile_number', 'address', 'cv', 'profile_pic']
    readonly_fields = ['user']  

admin.site.register(Doctor, DoctorAdmin)

