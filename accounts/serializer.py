from .models import User,Profile
from rest_framework import serializers
from django.db import models

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','password','phone','Address1','Address2','pincode']
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'