from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='sec_home'),

    path('login/', views.login_user, name='button1'),
    path('logout/', views.logout_user, name='button2'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/',views.dashboard, name= 'dashboard'),


    path('add_availability/', views.add_availability, name='add_availability'),
    path('delete-time-slot/<int:slot_id>/', views.delete_time_slot, name='delete_time_slot'),
    path('available-doctors/', views.available_doctors, name='available_doctors'),
    path('available-doctors/<str:department>/', views.available_doctors, name='available_doctors_by_department'),

    path('add_profile/', views.add_profile, name='add_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_profile_patient/', views.update_profile_patient, name='update_profile_patient'),


    path('book-appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('confirm-booking/<int:doctor_id>/<int:timeslot_id>/', views.confirm_booking, name='confirm_booking'),

    path('view-appointments-patient/', views.view_appointments_patient, name='view_appointments_patient'),

]
    


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
