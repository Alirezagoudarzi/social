from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirmpassword=forms.CharField(label='Confirm Password' , widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exist!')
        
        return email 


    def clean_username(self):
        username=self.cleaned_data['username']
        user=User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username already exist!')
        
        return username


    def clean(self):
        cd = super().clean() # اون سه تا تابع ارزیابی رو صدا میزنه و کلین دیتا رو میسازه
        p1=cd.get('password')
        p2=cd.get('confirmpassword')

        if p1 and p2 and p1 != p2:
            raise ValidationError('Password and confirm password must be mach!')
        
        
class UserLoginForm(forms.Form):
    username=forms.CharField(label='Username or Email address' ,widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

