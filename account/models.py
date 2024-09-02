from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=300,null=True)
    body=models.TextField()
    slug=models.SlugField()
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.slug