from django.contrib import admin
from .models import CustomUser
from .models import Doctor


# Register your models here.

class customUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']
    search_fields = ['username', 'email', 'role']
    list_filter = ['role']
    fields = ['username', 'email', 'role', 'password']
    readonly_fields = ['password']

admin.site.register(CustomUser,customUserAdmin) 




# to approve the doctors
@admin.action(description='Approve selected doctors')
def approve_doctors(modeladmin, request, queryset):
    queryset.update(is_approved=True)


# to view the doctor objects
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'department', 'mobile_number', 'address', 'is_approved']
    search_fields = ['user__username', 'full_name', 'department']
    list_filter = ['department', 'is_approved']
    fields = ['user', 'department', 'full_name', 'mobile_number', 'address', 'cv', 'profile_pic', 'is_approved']
    readonly_fields = ['user']
    actions = [approve_doctors] 

admin.site.register(Doctor, DoctorAdmin)



