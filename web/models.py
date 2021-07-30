from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings

from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

# Create your models here.

class Token(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    token = models.CharField(max_length = 48)

    def __str__(self):
        return '{}-token'.format(self.user)

class Expense(models.Model):
    text = models.CharField(max_length = 255)
    amount = models.BigIntegerField()
    date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.text, self.amount)

class Income(models.Model):
    text = models.CharField(max_length = 255)
    date = models.DateTimeField()
    amount = models.BigIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    def __str__(self): 
        return '{}-{}'.format(self.text, self.amount)




################### custom User #######################################

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email