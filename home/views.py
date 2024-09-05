from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Post,CommentModel

from .form import PostUpdateForm,PostCreateForm,CommentCreateForm


# Create your views here.
class HomeView(View):
    def get(self,request):
        posts=Post.objects.all()
        return render(request,'home/index.html',{'posts':posts})
    

class PostDetailView(View):

    form_class=CommentCreateForm

    def get(self,request,post_id,post_slug):
        post=get_object_or_404(Post,pk=post_id,slug=post_slug) # post=Post.objects.get(pk=post_id,slug=post_slug)
        comments=post.pcomments.filter(is_reply=False) #comment asli hastan ro biyar na comment haie reply ro
        return render(request,'home/detail.html',{'post':post,'comments':comments,'form':self.form_class})

    @method_decorator(login_required)
    def post(self,request,post_id,post_slug):
            form=self.form_class(request.POST)
            post_instance=get_object_or_404(Post,pk=post_id,slug=post_slug)
            if form.is_valid():
                new_comment=form.save(commit=False)
                new_comment.user=request.user
                new_comment.post= post_instance
                new_comment.save()
                messages.success(request,'your comment submited successfully.','success')
                return redirect('home:post_detail',post_id,post_slug)



class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post=get_object_or_404(Post,pk=post_id)
        # post=Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request,'Post successfully deleted.','success')
        else:
            messages.error(request,'you can\'t delete this post','danger')
        
        return redirect('home:home')




class PostUpdateView(View):
    
    form_class=PostUpdateForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.post_instance=get_object_or_404(Post,id=kwargs['post_id'])
        # self.post_instance=Post.objects.get(id=kwargs['post_id'])
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
        

class PostCreateView(LoginRequiredMixin,View):
    form_class= PostCreateForm

    def get(self,request):
        form=self.form_class
        return render(request,'home/create.html',{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.user=request.user
            new_post.slug=slugify(new_post.title)
            new_post.save()
            messages.success(request,'New post created successfully','success')
            return redirect('home:post_detail',new_post.id,new_post.slug)
        










