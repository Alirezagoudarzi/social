from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .form import PostUpdateForm
from django.utils.text import slugify


# Create your views here.
class HomeView(View):
    def get(self,request):
        posts=Post.objects.all()
        return render(request,'home/index.html',{'posts':posts})
    

class PostDetailView(View):
    def get(self,request,post_id,post_slug):
        post=Post.objects.get(pk=post_id,slug=post_slug)
        return render(request,'home/detail.html',{'post':post})


class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post=Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request,'Post successfully deleted.','success')
        else:
            messages.error(request,'you can\'t delete this post','danger')
        
        return redirect('home:home')




class PostUpdateView(View):
    form_class=PostUpdateForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.post_instance=Post.objects.get(id=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post=self.post_instance
        if not (request.user.id == post.user.id):
            messages.error(request,'you can\'t update this post.','danger')
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)
    

    def get(self,request,*args, **kwargs):
        post=self.post_instance
        form=self.form_class(instance=post)
        return render (request,'home/update.html',{'form':form})

    def post(self,request,post_id,*args, **kwargs):
        post=self.post_instance
        form=self.form_class(request.POST,instance=post)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug=slugify(new_post.title)
            new_post.save()
            messages.success(request,'update successfully','success')
            return redirect('home:post_detail' ,post.id,post.slug)