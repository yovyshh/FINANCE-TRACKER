from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from . models import *
from . forms import *
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
import secrets
import string
from .forms import RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import User  
from django.views.generic import TemplateView
from django.http import JsonResponse
import json
import requests
import os
import re


# Create your views here.
def index(request):
    return render(request,'index.html')


#User Login
def doLogin(request):
    form = LoginForm()
    if request.method == "POST":
        user = authenticate(request,username=request.POST["username"],password=request.POST["password"] )
        if user is None:
            return render(request,'index.html',{'form':form,'k':True})   
        else:
            login(request, user)
            data = users.objects.get(username=user)
            request.session['ut']=data.usertype
            request.session['uid']=data.id
            messages.success(request, f'Login Successfull!! Welcome {data.username}', extra_tags='log')
            return redirect('/')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})  


#User Logout
def logout(request):
    auth.logout(request)                
    return redirect('/') 



#User ForgotPassword
def forgotpswd(request):
    return render(request, 'forgotpswd.html', {'user': request.user})


#User Profile
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


#User Generate Password
def generate_random_password(length=6):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


#User Reset Password
def reset_password(request):
    if request.method == "POST":
                user = users.objects.get(username=request.POST['username'])
                new_password = generate_random_password()
                user.password = make_password(new_password)
                user.save()
                subject = 'password'
                message = "your password is " + str(new_password)
                email_from = settings.EMAIL_HOST_USER
                recepient_list = [user.email]  
                send_mail(subject,message,email_from,recepient_list)
    else:
        return render(request,"forgotpswd.html")
    return redirect('/login')


#User Update Profile
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data['email']
            if users.objects.filter(email=email).exclude(id=request.user.id).exists():
                form.add_error('email', 'Email already exists')
            else:
                try:
                    user = form.save(commit=False)
                    if form.cleaned_data.get('password'):
                        user.password = make_password(form.cleaned_data['password'])
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Profile updated successfully.')
                    return redirect('/profile')
                except Exception as e:
                    form.add_error(None, f'An error occurred while updating the profile: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {
            'username': request.user.username,
            'email': request.user.email,
            'place': request.user.place,
            'phone': request.user.phone,
            'image': request.user.image
        }
        form = ProfileForm(initial=initial_data, instance=request.user)
    return render(request, 'update_form.html', {'form': form})


#User Change Password
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            try:
                user = form.save()
                update_session_auth_hash(request, user)  
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('/login')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password_change_form.html', {'form': form})


# ListView
class MyModelListView(ListView):
    model = users
    template_name = 'model_list.html'  
    context_object_name = 'mymodels'

    def get_queryset(self):
        return users.objects.filter(is_superuser=False)


# updateview
class MyModelUpdateView(UpdateView):
    model = users
    form_class = UserForm
    template_name = 'model_update.html'
    context_object_name = 'mymodels'
    success_url = reverse_lazy('model_list')


# CreateView
class MyModelCreateView(CreateView):
    model = users
    form_class = UserForm             
    template_name = 'model_create.html'
    success_url = reverse_lazy('model_list') 


    

class SelectViews(TemplateView):
    template_name = 'page.html'
    
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        
        if form.is_valid():
            email = form.cleaned_data.get("email")
            
            # Check if user with this email already exists
            if users.objects.filter(email=email).exists():
                messages.error(request, 'A user with this email already exists. Please login or use another email.')
                return render(request, 'register.html', {'form': form})

            try:
                # Save user with hashed password
                user_instance = form.save(commit=False)
                user_instance.password = make_password(form.cleaned_data['password'])  # Hash the password
                user_instance.usertype = 0  # Default usertype; adjust as needed
                user_instance.save()

                # Success message and redirect
                messages.success(request, 'Your registration has been successful! You can now log in.')
                return redirect('/login')
                
            except Exception as e:
                form.add_error(None, f'An error occurred while saving the form: {e}')
                return render(request, 'register.html', {'form': form})
        else:
            # Form is not valid; re-render with errors
            return render(request, 'register.html', {'form': form})
    
    # GET request
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def contact(request):
    return render(request,'contact.html')

def financial_services(request):
    return render(request, 'financial_services.html')



LLAMA_API_URL = "http://localhost:11434/api/generate"
CODE_STORAGE_PATH = "generated_code/"

if not os.path.exists(CODE_STORAGE_PATH):
    os.makedirs(CODE_STORAGE_PATH)
# Llama API URL
LLAMA_API_URL = "http://localhost:11434/api/generate"

def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data,"data")
            user_message = data.get("message", "").strip()
            print(user_message,"user_message")
            if not user_message:
                return JsonResponse({"error": "No message received"}, status=400)

            prompt = f"Respond correctly to the user query:\n\n{user_message}"
            # Prepare request for Llama API
            payload = {
                "model": "llama3.2",
                "prompt": prompt,
                "max_tokens": 150,
                "temperature": 0.7,
                "stream": False
            }
            print(payload,"payload")
            headers = {"Content-Type": "application/json"}
            print(headers,"header")

            # Send request to Llama API
            try:
                response = requests.post(LLAMA_API_URL, headers=headers, json=payload)
                print(f"Response Status: {response.status_code}, Response Text: {response.text}")

                if response.status_code != 200 or not response.text.strip():
                    return JsonResponse(
                        {"error": "Invalid response from Llama API", "details": response.text},
                        status=500
                    )

                response_data = response.json()
                bot_reply = response_data.get("response", "").strip()

                return JsonResponse({"reply": bot_reply})

            except requests.exceptions.RequestException as e:
                return JsonResponse({"error": "Failed to connect to Llama API", "details": str(e)}, status=500)
            except ValueError as e:
                return JsonResponse({"error": "Invalid JSON response from Llama API", "details": str(e)}, status=500)


        except Exception as e:
            return JsonResponse({"error": "Error processing request", "details": str(e)}, status=500)

    return render(request, "chat.html")