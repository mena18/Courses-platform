from django.db import models


from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)