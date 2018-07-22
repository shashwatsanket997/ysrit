from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from django.core.validators import RegexValidator
import os
# Create your models here.
class Mandal(models.Model):
    mandal=models.CharField(max_length=500)
    def __str__(self):
        return self.mandal

class GramPanchayat(models.Model):
    mandal=models.ForeignKey(Mandal,on_delete=models.CASCADE)
    gp=models.CharField(max_length=500)
    def __str__(self):
        return self.gp

class Village(models.Model):
    gp=models.ForeignKey(GramPanchayat,on_delete=models.CASCADE)
    village=models.CharField(max_length=500)
    def __str__(self):
        return self.village

class  PartyPosition(models.Model):
    party_position=models.CharField(max_length=100)
    def __str__(self):
        return self.party_position


class Constency(models.Model):
    mandal=models.CharField(max_length=500,blank=True)
    gram_panchayat=models.CharField(max_length=500,blank=True)
    village=models.CharField(max_length=500,blank=True)
    def __str__(self):
        return(self.mandal)



class Party(models.Model):
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number should be up to 10 digits only")
    name=models.CharField(max_length=500)
    father_name=models.CharField(max_length=500,default='')
    dob=models.DateField(null=True,blank=True)
    phone_number=models.CharField(validators=[phone_regex],max_length=13,default='')
    booth_number=models.CharField(max_length=10,default='')
    mandal=models.ForeignKey(Mandal,on_delete=models.SET_NULL,null=True)
    gram_panchayat=models.ForeignKey(GramPanchayat,on_delete=models.SET_NULL,null=True)
    village=models.ForeignKey(Village,on_delete=models.SET_NULL,null=True)
    party_position=models.ForeignKey(PartyPosition,on_delete=models.SET_NULL,null=True)
    profile=models.ImageField(upload_to='partydata/',null=True,blank=True)
    def __str__(self):
        return self.name
class PartyFilter(models.Model):
    mandal=models.ForeignKey(Mandal,on_delete=models.SET_NULL,null=True,blank=True)
    gram_panchayat=models.ForeignKey(GramPanchayat,on_delete=models.SET_NULL,null=True,blank=True)
    village=models.ForeignKey(Village,on_delete=models.SET_NULL,null=True,blank=True)
    party_position=models.ForeignKey(PartyPosition,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.name
    

class Smsapi(models.Model):
    sam_api=models.CharField(max_length=250)

    def __str__(self):
        return self.sam_api
