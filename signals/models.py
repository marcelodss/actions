from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# https://docs.djangoproject.com/en/4.0/ref/signals/
# https://docs.djangoproject.com/en/4.0/topics/signals/


class Profile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'{self.usuario.username} / {self.usuario.first_name} - {self.usuario.last_name}'

