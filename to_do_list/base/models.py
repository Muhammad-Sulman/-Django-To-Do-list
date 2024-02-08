from django.db import models
from django.contrib.auth.models import User # django have built-in model for user which includes user information like name ,email,password etc. so we make one-to-many relation 1 user can do many things

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)#if admin delete or in future user want to delete account so what happen to record decides (on_delete) attribute. this field can be null and can be blank no need to input data in form if user want.
    tittle = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)# automatically adds the current time no need to enter manually in form

    def __str__(self) -> str:
        return self.tittle
    
    class Meta:
        ordering = ['complete']


