from django import forms
from django.contrib.auth.models import User


from .models import Constency,Mandal,GramPanchayat,Village,Party,PartyFilter,PartyPosition,Smsapi


class ConstencyForm(forms.ModelForm):

    class Meta:
        model = Constency
        fields = ['mandal', 'gram_panchayat', 'village']

class PartyForm(forms.ModelForm):
    class Meta:
        model=Party
        fields=['name','father_name','gender','dob','caste','voter_id','phone_number','booth_number','mandal', 'gram_panchayat', 'village','party_position','profile']
        
    def __init__(self, user, *args, **kwargs):
        super(PartyForm, self).__init__(*args, **kwargs)
        if(not user.is_superuser):
            self.fields['mandal'].queryset = Mandal.objects.filter(user=user)
            self.fields['gram_panchayat'].queryset = GramPanchayat.objects.filter(user=user)
            self.fields['village'].queryset = Village.objects.filter(user=user)
            self.fields['party_position'].queryset = PartyPosition.objects.filter(user=user)
            
            
                
class FilterForm(forms.ModelForm):
    class Meta:
        model=PartyFilter
        fields=['mandal', 'gram_panchayat', 'village','party_position']

    def __init__(self, user, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        if(not user.is_superuser):
            self.fields['mandal'].queryset = Mandal.objects.filter(user=user)
            self.fields['gram_panchayat'].queryset = GramPanchayat.objects.filter(user=user)
            self.fields['village'].queryset = Village.objects.filter(user=user)
            self.fields['party_position'].queryset = PartyPosition.objects.filter(user=user)

class Partypos(forms.ModelForm):
    class Meta:
        model=PartyPosition
        fields=['party_position']

class smsapiform(forms.ModelForm):
    class Meta:
        model=Smsapi
        fields=['sam_api']

    

