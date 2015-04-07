from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=30, blank=True)
    job = models.CharField(max_length=84, blank=True)
    department = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


def user_post_save(sender, instance, **kwargs):
    ( profile, new ) = UserProfile.objects.get_or_create(user=instance)


models.signals.post_save.connect(user_post_save, sender=User)