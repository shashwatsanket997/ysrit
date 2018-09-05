from django import forms
from django.contrib.auth.models import User

from .models import Constency,Mandal,GramPanchayat,Village,Party,PartyFilter,PartyPosition,Smsapi,MP


def check_mp(user):
    try:
        mp_user=MP.objects.get(mp=user)
    except MP.DoesNotExist:
        return ([False,None])
    constency=mp_user.Constensies.all()
    return ([True,constency])



class ConstencyForm(forms.ModelForm):

    class Meta:
        model = Constency
        fields = ['user','mandal', 'gram_panchayat', 'village']
    def __init__(self, user, *args, **kwargs):
        super(ConstencyForm, self).__init__(*args, **kwargs)
        check=check_mp(user)
        is_mp=check[0]
        ctnc=check[1]
        if(is_mp):
            self.fields['user'].queryset=ctnc
        elif(not (user.is_superuser or is_mp)):
            self.fields.pop('user')

    


class PartyForm(forms.ModelForm):
    class Meta:
        model=Party
        fields=['user','name','father_name','age','caste','phone_number','voter_id','booth_number','mandal', 'gram_panchayat', 'village','party_position','profile']
        
    def __init__(self, user, *args, **kwargs):
        super(PartyForm, self).__init__(*args, **kwargs)
        check=check_mp(user)
        is_mp=check[0]
        ctnc=check[1]
        if(is_mp):
            self.fields['mandal'].queryset = Mandal.objects.filter(user__in=ctnc)
            self.fields['gram_panchayat'].queryset = GramPanchayat.objects.filter(user__in=ctnc)
            self.fields['village'].queryset = Village.objects.filter(user__in=ctnc)
            self.fields['party_position'].queryset = PartyPosition.objects.filter(user__in=ctnc)
            self.fields['user'].queryset=ctnc

        elif(not user.is_superuser):
            self.fields['mandal'].queryset = Mandal.objects.filter(user=user)
            self.fields['gram_panchayat'].queryset = GramPanchayat.objects.filter(user=user)
            self.fields['village'].queryset = Village.objects.filter(user=user)
            self.fields['party_position'].queryset = PartyPosition.objects.filter(user=user)
            self.fields.pop('user')
            
                
class FilterForm(forms.ModelForm):
    class Meta:
        model=PartyFilter
        fields=['user','mandal', 'gram_panchayat', 'village','party_position']

    def __init__(self, user, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        check=check_mp(user)
        is_mp=check[0]
        ctnc=check[1]
        if(is_mp):
            self.fields['user'].queryset=ctnc
            self.fields['mandal'].queryset = Mandal.objects.filter(user__in=ctnc)
            self.fields['gram_panchayat'].queryset = GramPanchayat.objects.filter(user__in=ctnc)
            self.fields['village'].queryset = Village.objects.filter(user__in=ctnc)
            self.fields['party_position'].queryset = PartyPosition.objects.filter(user__in=ctnc)
        elif(not user.is_superuser):
            self.fields.pop('user')
            self.fields['mandal'].queryset = Mandal.objects.filter(user=user)
            self.fields['gram_panchayat'].queryset = GramPanchayat.objects.filter(user=user)
            self.fields['village'].queryset = Village.objects.filter(user=user)
            self.fields['party_position'].queryset = PartyPosition.objects.filter(user=user)
            
class Partypos(forms.ModelForm):
    class Meta:
        model=PartyPosition
        fields=['user','party_position']
    def __init__(self, user, *args, **kwargs):
        super(Partypos, self).__init__(*args, **kwargs)
        check=check_mp(user)
        is_mp=check[0]
        ctnc=check[1]
        if(is_mp):
            self.fields['user'].queryset=ctnc
        elif(not (user.is_superuser or is_mp)):
            self.fields.pop('user')

class Mandal_form(forms.ModelForm):
    class Meta:
        model=Mandal
        fields=['mandal']

class gp_form(forms.ModelForm):
    class Meta:
        model=GramPanchayat
        fields=['mandal','gp']

class village_form(forms.ModelForm):
    class Meta:
        model=Village
        fields=['gp','village']



class smsapiform(forms.ModelForm):
    class Meta:
        model=Smsapi
        fields=['sam_api']


class MP_form(forms.ModelForm):
    class Meta:
        model=MP
        fields=['name','mp','Constensies']
        widgets = {
            'Constensies': forms.CheckboxSelectMultiple,
        }


