from django import forms
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.hashers import make_password
from .models import users
from django import forms
from .models import users 



#Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = users
        fields = [ 'email', 'phone', 'place','image']
        widgets = {         
            "email" : forms.EmailInput,
            "phone" : forms.TextInput,
            "place" : forms.TextInput
           }
        help_texts={
            "username":None
        }


#Login Form
class LoginForm(forms.ModelForm):
    class Meta:
        model = users
        fields = ['username', 'password']
        widgets = {
            "username" : forms.TextInput,
            "password": forms.PasswordInput(),
           }
        help_texts = {'username':None}


#Forgot Password Form
class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,  
        widget=forms.TextInput(attrs={'class': 'form-group'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


#PasswordChange Form
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label="Confirm New Password"
    )
    
    
    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValidationError("The password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("The password must contain at least one digit.")
        if not any(char.isalpha() for char in password):
             raise ValidationError("The password must contain at least one letter.")
        
        # Add custom validation logic here
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        self.validate_password(new_password1)
        return new_password1
       
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")

        # Ensure the new password is different from the old password
        if old_password and new_password1 and old_password == new_password1:
            self.add_error('new_password1', "The new password must be different from the old password.")
        return cleaned_data

#User Form
class UserForm(forms.ModelForm):
    class Meta:
        model = users
        fields = ['username', 'email', 'phone', 'place']
        help_texts = {'username':None}

 # Make sure to import your custom users model
 
DISTRICTS_CHOICES = [
    ('Alappuzha', 'Alappuzha'),
    ('Ernakulam', 'Ernakulam'),
    ('Idukki', 'Idukki'),
    ('Kannur', 'Kannur'),
    ('Kasaragod', 'Kasaragod'),
    ('Kollam', 'Kollam'),
    ('Kottayam', 'Kottayam'),
    ('Kozhikode', 'Kozhikode'),
    ('Malappuram', 'Malappuram'),
    ('Palakkad', 'Palakkad'),
    ('Pathanamthitta', 'Pathanamthitta'),
    ('Thiruvananthapuram', 'Thiruvananthapuram'),
    ('Thrissur', 'Thrissur'),
    ('Wayanad', 'Wayanad'),
]

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}), 
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), 
        label="Confirm Password"
    )
    image = forms.ImageField(
        required=False, 
        label="Profile Image",
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload your profile image'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}), 
        label="Username"
    )
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Full Name'}), 
        label="Full Name"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email Address'}), 
        label="Email"
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Address'}), 
        label="Address"
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}), 
        label="Phone"
    )
    place = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Place'}), 
        label="Place"
    )
    district = forms.ChoiceField(
        choices=DISTRICTS_CHOICES,
        widget=forms.Select(attrs={'placeholder': 'Select District'}),
        label="District"
    )

    class Meta:
        model = users  # Use the custom users model here
        fields = ['username', 'full_name', 'email', 'address', 'phone', 'place', 'district', 'password']
       
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data