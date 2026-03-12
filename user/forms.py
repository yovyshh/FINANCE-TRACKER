from django import forms
from .models import Register
from django.contrib.auth import authenticate

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['username', 'email','password','contact']
        widgets = {
            'username': forms.TextInput(attrs={'id':'username','required':True,'class':'input' ,'placeholder':'Enter you username'}),
            'email': forms.EmailInput(attrs={'id':'email','required':True,'class':'input' ,'placeholder':'Enter email'}),
            'password': forms.PasswordInput(attrs={'id':'password','required':True,'class':'input' ,'placeholder':'Enter password'}),
            'contact': forms.TextInput(attrs={'id':'contact','required':True,'class':'input' ,'placeholder':'Enter contact'}),
        }
        labels={
          'username':'',
          'email':'',
          'password':'',
          'contact':'',
        }
        help_texts={
          'username':None
        }
class SignInForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['username','password']
        widgets = {
            'username': forms.TextInput(attrs={'id':'username','required':True,'class':'input' ,'placeholder':'Enter you username'}),
             'password': forms.PasswordInput(attrs={'id':'password','required':True,'class':'input' ,'placeholder':'Enter password'}),
        }
        labels={
          'username':'',
          'password':'',
        }
        help_texts={
          'username':None,
        }