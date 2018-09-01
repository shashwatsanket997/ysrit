from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django_filters.views import FilterView
from . import views

app_name="cm"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('cmHome/',views.cmhome,name="cmhome"),
    path('login/',views.login_user,name="login"),
    path('create_constency/',views.create_constency,name='create-constency'),
    path('create_constency/import',views.constencyimport,name='constency-import'),
    path('create_constency/export',views.constencyexport,name='constency-export'),
    path('settings',views.Setsmsapi.as_view(),name='cm-settings'),
    path('logout/',views.logout_user,name="logout"),
    path('add/',views.PartyCreateView,name="person_add"),
    path('ajax/load-gram-panchayat/',views.load_gram_panchayat,name="ajax_load_gram_panchayat"),
    path('ajax/load-village/',views.load_village,name="ajax_load_village"),
    path('ajax/load-mandal/',views.load_mandal,name="ajax_load_mandal"),
    path('ajax/load-partyposition/',views.load_partyposition,name="ajax_load_partyposition"),
    path('partydata/',views.PartyDatabase.as_view(),name="partydata"),
    path('partydata/import/',views.partyimport,name="partydata-import"),
    path('partydata/filter/',views.filter_table,name="filter"),
    path('partydata/update/<int:pk>',views.PartyUpdateView.as_view(),name="update"),
    path('partydata/delete/<int:pk>/',views.PartyDelete.as_view(),name="party-delete"),
    path('partydata/export/<str:p_ids>/',views.partyexport,name="partydata-export"),
    path('partydata/export/',views.partycomp,name="database"),
    path('partydata/sample/',views.sample_download,name="sample-download"),
    path('constency/sample/',views.samplec_download,name="samplec-download"),
    path('sms',views.sms,name="smsmgt"),
    path('partyposition/',views.partypositionC.as_view(),name="partyposC"),
    path('partydata/gallery/',views.PartyDatabase_photo.as_view(),name="photo_manage"),
    path('partydata/filter-photo/',views.photo_manage,name="filter_photo"),
    path('partyposition/update/<int:pk>',views.PartyposUpdateView.as_view(),name="update_party_pos"),
    path('partyposition/delete/<int:pk>/',views.PartyposDelete.as_view(),name="partyposition-delete"),
    path('mandal/update/<int:pk>',views.MandalUpdateView.as_view(),name="update_mandal"),
    path('mandal/delete/<int:pk>/',views.MandalDelete.as_view(),name="mandal-delete"),
    path('grampanchayat/update/<int:pk>',views.GpUpdateView.as_view(),name="update_gp"),
    path('grampanchayat/delete/<int:pk>/',views.GpDelete.as_view(),name="gp-delete"),
    path('village/update/<int:pk>',views.VillageUpdateView.as_view(),name="update_village"),
    path('village/delete/<int:pk>/',views.VillageDelete.as_view(),name="village-delete"),

   
]
#path('login/',auth_views.login,{'template_name': 'cm/login.html'},name="login")
#path('add/',views.PersonCreateView.as_view(),name="person_add"),
# path('add/',views.PartyCreateView.as_view(),name="person_add"),