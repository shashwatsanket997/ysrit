from django.contrib import admin
from .models import Constency,Mandal,GramPanchayat,Village,Party,PartyPosition,Smsapi,MP
from .forms import MP_form
# Register your models here.


class ConstencyView(admin.ModelAdmin):
    list_display=('mandal','gram_panchayat','village')
    list_filter = ['mandal','gram_panchayat']
    search_fields=('mandal','gram_panchayat','village')
class PartyView(admin.ModelAdmin):
    list_display=('name','father_name','age','phone_number','mandal','gram_panchayat','village','party_position')
    list_filter = ['mandal','gram_panchayat','party_position']

admin.site.register(Constency,ConstencyView)

admin.site.register(Party,PartyView)
admin.site.register(PartyPosition)
admin.site.register(Mandal)
admin.site.register(GramPanchayat)
admin.site.register(Village)
admin.site.register(Smsapi)

class MPAdmin(admin.ModelAdmin):
    form = MP_form

admin.site.register(MP, MPAdmin)
