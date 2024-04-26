from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
# Create your models here.
def validate_mobile_numbers(value):
    pattern = r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
    if not re.match(pattern,value):
        raise ValidationError("please enter a valid mobile number!")

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10,validators=[validate_mobile_numbers])
    Address1 = models.TextField()
    Address2 = models.TextField()
    pincode = models.CharField(max_length=6)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user} Profile'