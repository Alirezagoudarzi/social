from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    title=models.CharField(max_length=300,null=True)
    body=models.TextField()
    slug=models.SlugField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=('-created',)

    def __str__(self) -> str:
        return self.slug
    
    def get_absolute_url(self):
        return reverse("home:post_detail", args=(self.id,self.slug))
    

class CommentModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='ucomments')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pcomments')
    reply=models.ForeignKey('CommentModel',on_delete=models.CASCADE,related_name='rcomments', null=True, blank=True)
    is_reply=models.BooleanField(default=False)
    body=models.TextField(max_length=500)
    created=models.DateTimeField

    def __str__(self) -> str:
        return f'{self.user} - {self.body[:30]}'














