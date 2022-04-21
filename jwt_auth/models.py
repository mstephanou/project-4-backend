from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# user avatars
class CustomUser(AbstractUser):
  image = models.CharField(max_length=200)