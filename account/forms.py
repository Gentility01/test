from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.db.models.base import Model
# from django.db import models
# from django.forms import fields

from account.models import Acount


class RegistrationForm(UserCreationForm):
    email  = forms.EmailField(max_length=255, help_text='Required. add a valid email address')

    class Meta:
        model = Acount
        fields = ('email', 'username', 'password1', 'password2')


# FORm VALIDATION 
    # EMAIL VALIDATION
    def clean_email(self):
        email = self.cleaned_data['email'].lower() # the email from ['email'] is from the name in email inputs in html

        try:
            account = Acount.objects.get(email=email)
        
        except Exception as e :
            return email
        raise forms.ValidationError(f"Email {email} is already in use")


    # username validation
    def clean_username(self):
        username = self.cleaned_data['username'] # the username from ['username'] is from the name in username inputs in html

        try:
            account = Acount.objects.get(username=username)
        
        except Exception as e :
            return username
        raise forms.ValidationError(f"Username {username} is already in use")


    


#  1. email validations and form validation
# note get function (in line 25 and 37)is going to return a single role (A particular field from the moels) but when we use something like  filter it will return a fields.Multiple role
# in this form validation we are checking if the email already exists and if it does it will trow back an error in line 26 it returns email in line 25
#same thing is applicable n the username





# BUILDING A CUSTOM LOGIN FORM( this is for loging user in)
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    class Meta:
        model = Acount
        fields = ('email', 'password')
        #genaral clean option
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email'] # the name ['email'] is from the name we gave to our html form
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Loging check your username and password and try again ")

