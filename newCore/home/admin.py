from django.contrib import admin
from .models import CustomUser
from .models import Doctor , Patient , TimeSlot , Appointment


# Register your models here.

class customUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'id','role']
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
    list_display = ['full_name', 'department', 'mobile_number', 'address', 'id','is_approved']
    search_fields = ['user__username', 'full_name', 'department']
    list_filter = ['department', 'is_approved']
    fields = ['user', 'department', 'full_name', 'mobile_number', 'address', 'cv', 'profile_pic', 'is_approved']
    readonly_fields = ['user']
    actions = [approve_doctors] 

admin.site.register(Doctor, DoctorAdmin)


class PatientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'mobile_number', 'address', 'id','profile_pic']
    search_fields = ['user__username', 'full_name']
    fields = ['user', 'full_name', 'mobile_number', 'address', 'profile_pic']
    readonly_fields = ['user']
   

admin.site.register(Patient, PatientAdmin)



class appointment_admin(admin.ModelAdmin):
    list_display = ['patient_full_name','doctor_full_name','time_slot', 'id','status']
    search_fields = ['patient__full_name','doctor__full_name','status']
    fields = ['time_slot','prescription','status']

    def patient_full_name(self, obj):
        return obj.patient.full_name

    def doctor_full_name(self, obj):
        return obj.doctor.full_name


    patient_full_name.short_description = 'Patient Full Name'
    doctor_full_name.short_description = 'Doctor Full Name'
    


admin.site.register(Appointment,appointment_admin)







