from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='button1'),
    path('logout/', views.logout_user, name='button2'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/',views.dashboard, name= 'dashboard'),

    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('delete-time-slot/<int:slot_id>/', views.delete_time_slot, name='delete_time_slot'),
    path('available-doctors/', views.available_doctors, name='available_doctors'),
    
    # path('doctor_dashboard/',views.doctor_dash,name='doctor_dash'),
    # path('patient_dashboard/',views.patient_dash , name='patient_dash'),
]