from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout , authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache



# home page
@never_cache
def home(request):
    return render(request, 'home.html')


# login view
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
    return render(request, 'login.html', {})


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
                return redirect('home')
            else:
                return redirect('signup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form}) 



# logout view
def logout_user(request):
    logout(request)
    return redirect('home')



# @login_required   
# def doctor_dash(request):
#       return render(request,'doctor-dashboard.html')
     
     
# @login_required
# def patient_dash(request):
#       return render(request,'patient-dashboard.html')