from django.db import models
from django.contrib.auth.models import User

 
 
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone= models.CharField(max_length=30, blank=True)
    job=models.CharField(max_length=84, blank=True)
    department=models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username
 
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'