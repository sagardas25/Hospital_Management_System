from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='button1'),
    path('logout/', views.logout_user, name='button2'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/',views.dashboard, name= 'dashboard'),

    # path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('add_availability/', views.add_availability, name='add_availability'),
    path('delete-time-slot/<int:slot_id>/', views.delete_time_slot, name='delete_time_slot'),
    path('available-doctors/', views.available_doctors, name='available_doctors'),
    path('update_profile/', views.update_profile, name='update_profile'),
    
    # path('doctor_dashboard/',views.doctor_dash,name='doctor_dash'),
    # path('patient_dashboard/',views.patient_dash , name='patient_dash'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
