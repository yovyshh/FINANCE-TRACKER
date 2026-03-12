from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import *


def viewuser(request):
  a=Register.objects.filter(usertype= 2)
  return render(request,'viewusers.html',{'a': a })


def category(request):
  form=CategoryForm(request.POST,request.FILES)
  if request.method=='POST':
    
    if form.is_valid():
      
      form.save()
      return redirect('/')
  else:
    form=CategoryForm()
    print("is not found")
  return render(request,'register.html',{'form':form,'title':'Add category'})

def viewcategory(request):
  a=IncomeCategory.objects.all()
  return render(request,'viewcategories.html',{'a': a })




  
