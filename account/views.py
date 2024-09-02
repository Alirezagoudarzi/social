from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate





# Create your views here.

class UserRegisterView(View):

    form_class=UserRegistrationForm
    template_name='account/register.html'

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


class UserLogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,'User logout successfully!','success')
        return redirect('home:home')