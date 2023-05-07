from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=20, validators=[RegexValidator(r'^[a-zA-Z0-9]+$'), MinLengthValidator(6)], unique=True)
    password = models.CharField(max_length=20, validators=[RegexValidator(r'^[ -~]+$'), MinLengthValidator(8)])
    nickname = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(max_length=500, null=True, blank=True)
