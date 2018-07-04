from django import forms
from django.contrib.auth.models import User


from .models import Constency,Mandal,GramPanchayat,Village,Party,PartyFilter


class ConstencyForm(forms.ModelForm):

    class Meta:
        model = Constency
        fields = ['mandal', 'gram_panchayat', 'village']

class PartyForm(forms.ModelForm):
    class Meta:
        model=Party
        fields=['name','father_name','dob','phone_number','booth_number','mandal', 'gram_panchayat', 'village','party_position','profile']
    
class FilterForm(forms.ModelForm):
    class Meta:
        model=PartyFilter
        fields=['mandal', 'gram_panchayat', 'village','party_position']


    
