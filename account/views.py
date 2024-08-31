from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.

class RegisterView(View):
    def get(self,request):
        form=UserRegistrationForm()
        return render(request,'account/register.html',{'form': form})

    def post(self,request):
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            User.objects.create_user(username=cd['username'],email=cd['email'],password=cd['password'])
            messages.success(request,'user registered successfully','success')
            return redirect('home:home')

