from django.shortcuts import render,redirect ,get_object_or_404
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse
from django.contrib.auth import login,logout , authenticate
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm 
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from . import forms
from .models import Doctor, TimeSlot, CustomUser , Patient , Appointment
from .forms import TimeSlotForm , DoctorProfileForm , PatientProfileForm
import calendar
from datetime import datetime , timedelta
from django.http import Http404






#home page
@never_cache
def home(request):
    return render(request, 'auth/home.html')


#login view
@never_cache
def login_user(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))  
                             
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')
            

        else:
            messages.error(request, "Invalid information. Please try again")

    return render(request, 'auth/login.html', {})



# sign up view
@never_cache
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))   
                            
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                if user.role == 'doctor':
                    Doctor.objects.create(user=user)

                if user.role == 'patient':
                    Patient.objects.create(user=user)

                if user.role == 'doctor':
                    return redirect('add_profile')
                
                elif user.role == 'patient' :
                    return redirect('add_profile_patient')

                else :

                 return redirect('home')
                

            else:
                return redirect('signup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/signup.html', {'form': form}) 



# logout view
@login_required
def logout_user(request):
    logout(request)
    return redirect('home')



@never_cache
@login_required
def dashboard(request):
    user = request.user 

    if user.role == 'doctor':

        if user.doctor.is_approved:   
            return render(request,'auth/65dashboard.html' , {'user' : user})
        else:
            raise Http404("You don't have enough permissions !!")
        
    else :
    
         return render(request,'auth/dashboard.html' , {'user' : user})



#########################################################################################################################

# patient related views
@never_cache
@login_required
def patient_dashboard(request):
    return render(request, 'dashboard.html')

@never_cache
@login_required
def available_doctors(request):
    if request.user.role != 'patient':
        return redirect('home')

   
    department = request.GET.get('department')

    if department:
        doctors = Doctor.objects.filter(department=department)
    else:
        doctors = Doctor.objects.all()

    doctor_slots = {doctor: TimeSlot.objects.filter(doctor=doctor).order_by('date', 'start_time') for doctor in doctors}

    return render(request, 'patient/available_doctors.html', {'doctor_slots': doctor_slots, 'selected_department': department})



@never_cache
@login_required
def update_profile_patient(request):

    try:
        patient = Patient.objects.get(user=request.user)

    except Patient.DoesNotExist:

        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')
    

    if request.method == 'POST':
        patient_profile_form = PatientProfileForm(request.POST, request.FILES, instance=patient)  

        if patient_profile_form.is_valid():
            patient_profile_form.save()
            # messages.success(request, 'Profile updated successfully.')
            return redirect('patient/update_profile_patient') 


    else:

        patient_profile_form = PatientProfileForm(instance=patient)


    return render(request, 'patient/update_profile_patient.html', {'patient_profile_form': patient_profile_form,})


@never_cache
@login_required
def add_profile_patient(request):

    
    if request.user.patient.full_name :
         return redirect ('home')
        

    try:
        patient = Patient.objects.get(user=request.user)

    except Patient.DoesNotExist:

        # messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')
    

    if request.method == 'POST':
        patient_profile_form = PatientProfileForm(request.POST, request.FILES, instance=patient)  

        if patient_profile_form.is_valid():
            patient_profile_form.save()
            # messages.success(request, 'Profile updated successfully.')
            return redirect('home')


    else:

        patient_profile_form = PatientProfileForm(instance=patient)


    return render(request, 'patient/update_profile_patient.html', {'patient_profile_form': patient_profile_form,})


@never_cache
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    slots = TimeSlot.objects.filter(doctor=doctor, booked=False).order_by('date', 'start_time')
    
    if request.method == 'POST':
        timeslot_id = request.POST.get('slot_id')
        timeslot = get_object_or_404(TimeSlot, id=timeslot_id)
        

        patient = get_object_or_404(Patient, user=request.user)
        age = request.POST['age']
        describe_problem = request.POST['describe_problem']


        timeslot.booked = True
        timeslot.patient = patient
        timeslot.save()


        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            time_slot=timeslot,
            date=timeslot.date,
            patient_age = age,
            describe_problem= describe_problem,
            status='pending'  # Set status to pending
        )

        return redirect('confirm_booking', doctor_id=doctor.id, timeslot_id=timeslot.id)

    return render(request, 'patient/book_appointment.html', {'doctor': doctor, 'slots': slots})


@never_cache
@login_required
def confirm_booking(request, doctor_id, timeslot_id):
    timeslot = get_object_or_404(TimeSlot, id=timeslot_id)
    return render(request, 'patient/booking_confirmation.html', {'timeslot': timeslot})


@never_cache
@login_required
def view_appointments_patient(request):

    patient = Patient.objects.get(user=request.user)
    status_filter = request.GET.get('status', 'all')
    
    if status_filter == 'pending':
        appointments = Appointment.objects.filter(patient=patient, status='pending')
    elif status_filter == 'accepted':
        appointments = Appointment.objects.filter(patient=patient, status='accepted')
    elif status_filter == 'cancelled':
        appointments = Appointment.objects.filter(patient=patient, status='cancelled')
    else:
        appointments = Appointment.objects.filter(patient=patient)
    
    return render(request, 'patient/view_appointments_patient.html', {'appointments': appointments, 'status_filter': status_filter})



@never_cache
@login_required
def active_appointments_patient(request):
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient, status='accepted')
    return render(request, 'patient/active_appointments_patient.html', {'appointments': appointments})


@never_cache
@login_required
def appointment_details_patient(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST' :
        feedback = request.POST.get('feedback')
        appointment.feedback = feedback
        appointment.save()

    return render(request, 'patient/appointment_details_patient.html', {'appointment': appointment})


#################################################################################################################################

# doctor related views

@login_required
@never_cache 
def add_availability(request):
    try:
        doctor = Doctor.objects.get(user=request.user,is_approved=True)
    except Doctor.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = TimeSlotForm(request.POST)

        if form.is_valid():

            day = int(form.cleaned_data['day'])
            selected_time_slots = form.cleaned_data['time_slots']

            for slot in selected_time_slots:

                start_time_str, end_time_str = slot.split('-') 
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()
                date = get_next_weekday(datetime.now(), day) 


                # Check if the time slot already exists
                if TimeSlot.objects.filter(doctor=doctor, date=date, start_time=start_time, end_time=end_time).exists():
                    messages.warning(request, 'time slot already exists.')
                else:
                    TimeSlot.objects.create(doctor=doctor, date=date, start_time=start_time, end_time=end_time)
                    # messages.success(request, f'Time slot {start_time_str} - {end_time_str} on {date.strftime("%Y-%m-%d")} added successfully.')



            return redirect('add_availability') 
    else:
        form = TimeSlotForm()

    time_slots = TimeSlot.objects.filter(doctor=doctor)
    slots_by_date = {} 

    for slot in time_slots:

        if slot.date not in slots_by_date:
            slots_by_date[slot.date] = []
        slots_by_date[slot.date].append(slot)


    return render(request, 'doctor/add_availability.html', {
        'form': form,
        'time_slots': time_slots,

    })



def get_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)



@never_cache
@login_required
def delete_time_slot(request, slot_id):
    time_slot = get_object_or_404(TimeSlot, id=slot_id)
    if time_slot.doctor.user != request.user:
        messages.error(request, 'You are not authorized to delete this time slot.')
        return redirect('add_availability')
    time_slot.delete()
    # messages.success(request, 'Time slot deleted successfully.')
    return redirect('add_availability')



@never_cache
@login_required
def add_profile(request):

    
    if request.user.doctor.full_name :
         return redirect ('home')
        

    try:
        doctor = Doctor.objects.get(user=request.user)

    except Doctor.DoesNotExist:

        # messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')
    

    if request.method == 'POST':
        profile_form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)  

        if profile_form.is_valid():
            profile_form.save()
            # messages.success(request, 'Profile updated successfully.')
            return redirect('home')


    else:

        profile_form = DoctorProfileForm(instance=doctor)


    return render(request, 'doctor/update_profile.html', {'profile_form': profile_form,})



@never_cache
@login_required
def update_profile(request):

    try:
        doctor = Doctor.objects.get(user=request.user)

    except Doctor.DoesNotExist:

        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')
    

    if request.method == 'POST':
        profile_form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)  

        if profile_form.is_valid():
            profile_form.save()
            # messages.success(request, 'Profile updated successfully.')
            return redirect('update_profile') 


    else:

        profile_form = DoctorProfileForm(instance=doctor)


    return render(request, 'doctor/update_profile.html', {'profile_form': profile_form,})



@never_cache
@login_required
def view_appointments_doctor(request):
    if request.method == "POST":
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')
        appointment = Appointment.objects.get(id=appointment_id)
        
        if action == 'accept':
            appointment.status = 'accepted'
        elif action == 'cancel':
            appointment.status = 'cancelled'
            appointment.time_slot.booked = False
            appointment.time_slot.save()
        
        appointment.save()
        return redirect('view_appointments_doctor')
    
    pending_appointments = Appointment.objects.filter(status='pending', doctor=request.user.doctor)
    return render(request, 'doctor/view_appointments_doctor.html', {'appointments': pending_appointments})


@never_cache
@login_required
def active_appointments(request):
    doctor = request.user.doctor 
    appointments = Appointment.objects.filter(doctor=doctor, status='accepted').order_by('date', 'time_slot__start_time')
    return render(request, 'doctor/active_appointments.html', {'appointments': appointments})


@never_cache
@login_required
def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        prescription = request.FILES.get('prescription')
        remarks = request.POST.get('remarks')

        if prescription:
            appointment.prescription = prescription
        appointment.remarks = remarks
        appointment.save() 

        return redirect('active_appointments')
    
    return render(request, 'doctor/appointment_details.html', {'appointment': appointment})

@never_cache
@login_required
def ongoing_treatment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'doctor/ongoing_treatment.html', {'appointment': appointment})



@never_cache
@login_required
def current_patients(request):
    doctor = request.user.doctor
    accepted_appointments = Appointment.objects.filter(doctor=doctor, status='accepted')
    patients = {appointment.patient for appointment in accepted_appointments}
    
    return render(request, 'doctor/current_patients.html', {'patients': patients})

@never_cache
@login_required
def patient_details(request, patient_id):
    doctor = request.user.doctor
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(doctor=doctor, patient=patient, status='accepted')
    
    return render(request, 'doctor/patient_details.html', {'patient': patient, 'appointments': appointments})



def view_doctor_profile(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctor/doctor_profile.html', {'doctor': doctor})


#################################################################################################################



from django.shortcuts import render
from .models import Appointment
import os
from dotenv import load_dotenv
load_dotenv()





import time
from agora_token_builder import RtcTokenBuilder

def generate_agora_token(channel_name, uid):
    appId =os.getenv('APP_ID')
    appCtf = os.getenv('APP_CERTIFICATE')
    expiration_time_in_seconds = 3600
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds
    role = 1  # RtcTokenBuilder.Role_Publisher
    token = RtcTokenBuilder.buildTokenWithUid(appId,appCtf,channel_name, uid, role, privilege_expired_ts)
    return token

@login_required
def video_chat(request, appointment_id ):

    if request.user.is_authenticated:

        user = request.user
        appointment = Appointment.objects.get(id=appointment_id)
        token = generate_agora_token(str(appointment.id), 0)  # 0 means the user has no specific UID

        context = {
            
            'appointment': appointment,
            'token': token,
            'user':user,
            'remote_user_fullname' : appointment.doctor.full_name if user.role == 'patient' else appointment.patient.full_name
            
            }
        return render(request, 'videoChat/video_chat.html', context = context)

    else :
        return HttpResponseRedirect('sec_home') 
