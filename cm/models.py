from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from django.core.validators import RegexValidator
import os
from django.contrib.auth.models import Permission,User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser



# Create your models here.
class Mandal(models.Model):
    user=models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    mandal=models.CharField(max_length=500)
    def __str__(self):
        return self.mandal

class GramPanchayat(models.Model):
    user=models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    mandal=models.ForeignKey(Mandal,on_delete=models.CASCADE)
    gp=models.CharField(max_length=500)
    def __str__(self):
        return self.gp

class Village(models.Model):
    user=models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    gp=models.ForeignKey(GramPanchayat,on_delete=models.CASCADE)
    village=models.CharField(max_length=500)
    def __str__(self):
        return self.village

class PartyPosition(models.Model):
    user=models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    party_position=models.CharField(max_length=100)
    def __str__(self):
        return self.party_position


class Constency(models.Model):
    user=models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    mandal=models.CharField(max_length=500,blank=True)
    gram_panchayat=models.CharField(max_length=500,blank=True)
    village=models.CharField(max_length=500,blank=True)
    def __str__(self):
        return(self.mandal)

GENDER_CHOICES = (
    ('Male','MALE'),
    ('Female', 'FEMALE'),
)


class Party(models.Model):
    user=models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number should be up to 10 digits only")
    name=models.CharField(max_length=500)
    father_name=models.CharField(max_length=500,null=True,blank=True)
    gender=models.CharField(max_length=6,choices=GENDER_CHOICES,null=True,blank=True)
    age=models.CharField(max_length=3,null=True,blank=True)
    caste=models.CharField(max_length=100,null=True,blank=True)
    phone_number=models.CharField(validators=[phone_regex],max_length=10,default='')
    voter_id=models.CharField(max_length=13,null=True,blank=True)
    booth_number=models.CharField(max_length=10,null=True,blank=True)
    mandal=models.ForeignKey(Mandal,on_delete=models.SET_NULL,null=True)
    gram_panchayat=models.ForeignKey(GramPanchayat,on_delete=models.SET_NULL,null=True,blank=True)
    village=models.ForeignKey(Village,on_delete=models.SET_NULL,null=True,blank=True)
    party_position=models.ForeignKey(PartyPosition,on_delete=models.SET_NULL,null=True)
    profile=models.ImageField(upload_to='partydata/',null=True,blank=True)
    def __str__(self):
        return self.name
class PartyFilter(models.Model):
    user=models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    mandal=models.ForeignKey(Mandal,on_delete=models.SET_NULL,null=True,blank=True)
    gram_panchayat=models.ForeignKey(GramPanchayat,on_delete=models.SET_NULL,null=True,blank=True)
    village=models.ForeignKey(Village,on_delete=models.SET_NULL,null=True,blank=True)
    party_position=models.ForeignKey(PartyPosition,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.name
    

class Smsapi(models.Model):
    user=models.ForeignKey(User, default=1,on_delete=models.CASCADE)
    sam_api=models.CharField(max_length=250)

    def __str__(self):
        return self.sam_api

class MP(models.Model):
    name=models.CharField(max_length=250,null=True,blank=True)
    mp=models.OneToOneField(User,related_name='MP',on_delete=models.CASCADE)
    Constensies=models.ManyToManyField(User)
    

    def __str__(self):
        return self.name