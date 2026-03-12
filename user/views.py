
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import *
from django.contrib import auth
def home(request):
  return render(request,'index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.usertype = 2  # Set user type
            reg.set_password(form.cleaned_data['password'])  # Hash password
            reg.save()
            return redirect('/signin')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'title': 'Create an Account'})



def signin(request):
  
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username,"usernme")
        password = request.POST.get('password')
        print(password,"pass")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            request.session['ut']=user.usertype
            request.session['userid']=user.id
            messages.success(request, 'You have successfully logged in.')
            return redirect('/')  # Redirect to the home page after login
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('/signin')  # Reload the sign-in page if login fails
    else:
      
      form=SignInForm()
      return render(request, 'register.html',{'form':form,'title':'SIGN IN'})


def viewuser(request):
    if request.user.is_authenticated and request.user.is_staff:
        a = Register.objects.filter(usertype=2)
        return render(request, 'viewusers.html', {'a': a})
    else:
        return redirect('login')  # Redirect unauthorized users

def dologout(request):
       auth.logout(request)
       return redirect('/')
     

def service(request):
    return render(request, 'service.html')
  
def about(request):
    return render(request, 'about.html')

def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def view_cat(request):
    return render(request, 'contact.html')


from django.contrib.sessions.backends.db import SessionStore

def login_view(request):
    # Example logic
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Set session key for user type
            if user.is_superuser:
                request.session['ut'] = 1  # Admin
            else:
                request.session['ut'] = 2  # Regular user
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'signin.html')



