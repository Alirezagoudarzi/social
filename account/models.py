from django.db import models
from django.contrib.auth.models import User

class RelationsModel(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.from_user} following {self.to_user}' 