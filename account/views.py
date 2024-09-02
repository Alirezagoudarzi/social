from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate






# Create your views here.

class UserRegisterView(View):

    form_class=UserRegistrationForm
    template_name='account/register.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            messages.error(request,'you are loggedin. this request is nat valid.','warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form': form})

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            User.objects.create_user(username=cd['username'],email=cd['email'],password=cd['password'])
            msg='user \'' + cd['username']+'\' registered successfully'
            messages.success(request,msg,'success')
            return redirect('home:home')
        else:
            return render(request,self.template_name,{'form': form})


class UserloginView(View):

    form_class=UserLoginForm
    template_name='account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request,'you are loggedin. this request is nat valid.','warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    


    def get(self,request):
        form=self.form_class 
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'User login successfully','success')
                return redirect('home:home')
            messages.error(request,'Username or Password is wrong!','warning')
            return render(request,self.template_name,{'form':form})


class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'User logout successfully!','success')
        return redirect('home:home')
    


class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=User.objects.get(pk=user_id)
        return render(request,'account/profile.html',{'user': user})




