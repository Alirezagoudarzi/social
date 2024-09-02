from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.

class RegisterView(View):

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


