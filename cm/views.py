from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import ConstencyForm ,PartyForm,FilterForm
from .models import Constency,Mandal,GramPanchayat,Village,Party,PartyFilter,PartyPosition
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
import datetime
from django.http import HttpResponse
import csv
from .resource import PartyResource
import json



# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'cm/login.html')
    else:
        return render(request,'cm/index.html')

def cmhome(request):
    if not request.user.is_authenticated:
        return render(request, 'cm/login.html')
    else:
        return render(request,'cm/contact_management.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'cm/index.html')
            else:
                return render(request, 'cm/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'cm/login.html', {'error_message': 'Invalid login'})
    return render(request, 'cm/login.html')

def logout_user(request):
    logout(request)
    return render(request, 'cm/login.html')




def create_constency(request):
    if not request.user.is_authenticated:
        return render(request, 'cm/login.html')
    form = ConstencyForm(request.POST or None)
    if form.is_valid():
        if(form.cleaned_data['mandal'] and form.cleaned_data['gram_panchayat'] and form.cleaned_data['village']):
            mandal=form.cleaned_data['mandal'].title()
            gp=form.cleaned_data['gram_panchayat'].title()
            village=form.cleaned_data['village'].title()
            inf=''
            updated=[]
            try:
                f1=Mandal.objects.get(mandal=mandal)
            except:
                f1=Mandal(mandal=mandal)
                f1.save()
                inf="New Mandal Created:-->"+mandal
                updated.append(inf)
            try:
                f2=GramPanchayat.objects.get(gp=gp)
            except:
                f2=GramPanchayat(mandal=f1,gp=gp)
                f2.save()
                inf="New GramPanchayat Created :-->"+gp+" for Mandal:-->"+f2.mandal.mandal
                updated.append(inf)
            try:
                f3=Village.objects.get(village=village)
            except:
                f3=Village(gp=f2,village=village)
                f3.save()
                inf="New Village created :-->"+village+" for GramPanchayat:-->"+f3.gp.gp+" of Mandal:-->"+f2.mandal.mandal
                updated.append(inf)
            constency=form.save(commit=True)
            constency.save()
            if(inf==''):
                context={"error_message":['Data already exist'],}
            else:
                context={"error_message":updated,}
            return render(request, 'cm/create_constency.html', context)
        else:   
            context={"error_message":["Please fill all the fields"],
            "form":form}
            return render(request, 'cm/create_constency.html', context)
            
    context = {
            "form": form,
    }
    return render(request, 'cm/create_constency.html', context)    

def constencyimport(request):
    if not request.user.is_authenticated:
        return render(request, 'cm/login.html')
    data = {}
    if "GET" == request.method:
        return render(request, "cm/constencyimport.html", data)
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            context={"error_message":["File is not csv type"]}
            return render(request, "cm/constencyimport.html", context)
        if csv_file.multiple_chunks():
            context={"error_message":["Uploaded file is too big."]}
            return render(request, "cm/constencyimport.html", context)
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[1:]
        updated=[]
        for line in lines:
            inf=''
            fields = line.split(",")
            if('' in fields):
                fields.remove('')
            if(len(fields)==3):
                try:
                    mandal=fields[0].rstrip('\r').title()
                    gp=fields[1].rstrip('\r').title()
                    village=fields[2].rstrip('\r').title()
                    try:
                        f1=Mandal.objects.get(mandal=mandal)
                    except:
                        f1=Mandal(mandal=mandal)
                        f1.save()
                        inf="New Mandal Created:-->"+mandal
                        updated.append(inf)
                    try:
                        f2=GramPanchayat.objects.get(gp=gp)
                    except:
                        f2=GramPanchayat(mandal=f1,gp=gp)
                        f2.save()
                        inf="New GramPanchayat Created :-->"+gp+" for Mandal:-->"+f2.mandal.mandal
                        updated.append(inf)
                    try:
                        f3=Village.objects.get(village=village)
                    except:
                        f3=Village(gp=f2,village=village)
                        f3.save()
                        inf="New Village created :-->"+village+" for GramPanchayat:-->"+f3.gp.gp+" of Mandal:-->"+f2.mandal.mandal
                        updated.append(inf)
                    if(inf==''):
                        updated.append("Data already exist:-->"+str(line))
                except:
                    updated.append("Got unexpected garbage value or unprocessed value at line number:->"+str(lines.index(line)))
                    
            else:
                updated.append("Got unexpected garbage value or unprocessed value at line number:->"+str(lines.index(line)))
        updated.append("-----------------Processing Completed-----------------")
        context={"error_message":updated
            }
        return render(request, "cm/constencyimport.html", context)    
    except:
        context={"error_message":["Some unexpected error occured. Please refresh the page"]}
        return render(request, "cm/constencyimport.html", context)

def constencyexport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Constencies.csv"'
    writer = csv.writer(response)
    obj=Village.objects.all()
    writer.writerow(['Mandal','Gram panchayat','Village'])
    for i in obj:
        gp=i.gp
        writer.writerow([gp.mandal.mandal,gp.gp,i.village])
    return(response)
       


class PartyCreateView(CreateView):
    model=Party
    template_name="cm/partycreateview.html"
    form_class=PartyForm
    success_url=reverse_lazy('cm:person_add')

def load_gram_panchayat(request):
    mandal_id=request.GET.get('mandal')
    gram_panchayat=GramPanchayat.objects.filter(mandal_id=mandal_id)
    return render(request,'cm/dd.html',{'gram_panchayat':gram_panchayat})

def load_village(request):
    gp_id=request.GET.get('gram_panchayat')
    village =Village.objects.filter(gp_id=gp_id)
    return render(request,'cm/vv.html',{'village':village})


class PartyDatabase(ListView):
    model=Party
    template_name="cm/tables.html"


class PartyUpdateView(UpdateView):
    model=Party
    template_name="cm/partyupdateview.html"
    form_class=PartyForm
    success_url=reverse_lazy('cm:partydata')
    context_object_name='form'
    def get_context_data(self,**kwargs):
        context=super(PartyUpdateView,self).get_context_data(**kwargs)
        context['pk']=self.object.id
        print(context['pk'])
        return context


class PartyDelete(DeleteView):
    model=Party
    success_url=reverse_lazy('cm:partydata')

object_list=Party.objects.all()

def filter_table(request):
    form = FilterForm(request.POST or None)
    if form.is_valid():
        m1=request.POST.get('mandal')
        m2=request.POST.get('gram_panchayat')
        m3=request.POST.get('village')
        m4=request.POST.get('party_position')
        #object_list=Party.objects.filter(mandal_id=m1,gram_panchayat_id=m2,village_id=m3,party_position_id=m4)
        if(m1=='' and m2=='' and m3=='' and m4==''):
            context={
            "object_list":Party.objects.all(),
            "error_message":"Please choose some option",
            "form":form,
            "p_ids":'None' 
            }
            return render(request, 'cm/tables.html', context)
        
        elif(m1=='' and m2=='' and m3=='' and m4!=''):
            object_list=Party.objects.filter(party_position_id=m4)
        elif(m1=='' and m2=='' and m3!='' and m4==''):
            object_list=Party.objects.filter(village_id=m3)
        elif(m1=='' and m2=='' and m3!='' and m4!=''):
            object_list=Party.objects.filter(village_id=m3,party_position_id=m4)
        elif(m1=='' and m2!='' and m3=='' and m4==''):
            object_list=Party.objects.filter(gram_panchayat_id=m2)
        elif(m1=='' and m2!='' and m3=='' and m4!=''):
            object_list=Party.objects.filter(gram_panchayat_id=m2,party_position_id=m4)
        elif(m1=='' and m2!='' and m3!='' and m4==''):
            object_list=Party.objects.filter(gram_panchayat_id=m2,village_id=m3)
        elif(m1=='' and m2!='' and m3!='' and m4!=''):
            object_list=Party.objects.filter(gram_panchayat_id=m2,village_id=m3,party_position_id=m4)
        elif(m1!='' and m2=='' and m3=='' and m4==''):
            object_list=Party.objects.filter(mandal_id=m1)
        elif(m1!='' and m2=='' and m3=='' and m4!=''):
            object_list=Party.objects.filter(mandal_id=m1,party_position_id=m4)
        elif(m1!='' and m2=='' and m3!='' and m4==''):
            object_list=Party.objects.filter(mandal_id=m1,village_id=m3)
        elif(m1!='' and m2=='' and m3!='' and m4!=''):
            object_list=Party.objects.filter(mandal_id=m1,village_id=m3,party_position_id=m4)
        elif(m1!='' and m2!='' and m3=='' and m4==''):
            object_list=Party.objects.filter(mandal_id=m1,gram_panchayat_id=m2)
        elif(m1!='' and m2!='' and m3=='' and m4!=''):
            object_list=Party.objects.filter(mandal_id=m1,gram_panchayat_id=m2,party_position_id=m4)
        elif(m1!='' and m2!='' and m3!='' and m4==''):
            object_list=Party.objects.filter(mandal_id=m1,gram_panchayat_id=m2,village_id=m3)
        else:
            object_list=Party.objects.filter(mandal_id=m1,gram_panchayat_id=m2,village_id=m3,party_position_id=m4)
        p_ids=[i.id for i in object_list]  
        p_ids=str(p_ids) 
        context={
            "object_list":object_list,
            "error_message":"You Activated the filter",
            "form":form,
            "p_ids":p_ids
        }
        return render(request, 'cm/tables.html', context)
    else:
        context={
            "object_list":Party.objects.all(),
            "form":form ,
            "p_ids":"None"
        }
        return render(request, 'cm/tables.html', context)

def partyimport(request):
    data={}
    if "GET" == request.method:
        return render(request, "cm/partyimport.html", data)
    else:
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            context={"error_message":["File is not csv type"]}
            return render(request, "cm/partyimport.html", context)
        if csv_file.multiple_chunks():
            context={"error_message":["Uploaded file is too big."]}
            return render(request, "cm/partyimport.html", context)
        #CSV file error handled
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[1:]
        updated=[]
        for line in lines:                        
            fields = line.split(",")
            if('' in fields):
                fields.remove('')
            if(len(fields)==9):
                data_dict = {}
                try:
                    data_dict["name"] = fields[0].rstrip('\r').title()
                    data_dict["father_name"] = fields[1].rstrip('\r').title()
                    #12/5/2015
                    #12-05-2015
                    if("/" in fields[2]):
                        dt=fields[2].split('/')
                        date=dt[2]+"-"+dt[1]+"-"+dt[0]
                    else:
                        date=fields[2]
                    data_dict["dob"] = date
                    data_dict["phone_number"] = fields[3].rstrip('\r')
                    data_dict["booth_number"] = fields[4].rstrip('\r')
                    mandal=fields[5].rstrip('\r').title()
                    gp=fields[6].rstrip('\r').title()
                    village=fields[7].rstrip('\r').title()
                    print(fields)

                    try:
                        f1=Mandal.objects.get(mandal=mandal)
                    except:
                        #f1=Mandal(mandal=mandal)
                        #f1.save()
                        f1=''
                        inf="New Mandal found :-->"+mandal
                        updated.append(inf)
                    try:
                        f2=GramPanchayat.objects.get(gp=gp)
                    except:
                        #f2=GramPanchayat(mandal=f1,gp=gp)
                        #f2.save()
                        f2=''
                        inf="New GramPanchayat found :-->"+gp+ "for mandal :-->" +mandal
                        updated.append(inf)
                    try:
                        f3=Village.objects.get(village=village)
                    except:
                        #f3=Village(gp=f2,village=village)
                        #f3.save()
                        f3=''
                        inf="New Village found :-->"+village+" for GramPanchayat:-->"+gp+" of Mandal:-->"+mandal
                        updated.append(inf)
                    party_position=fields[8].rstrip("\r").title()
                    try:
                        party_position=PartyPosition.objects.get(party_position=party_position)
                    except:
                        #party_position=PartyPosition(party_position=party_position)
                        #party_position.save()
                        party_position=''
                        inf="New party positon found:-->"+party_position
                    if( f1!='' and f2!='' and f3!='' and party_position!=''):
                        data_dict["mandal"] = f1
                        data_dict["gram_panchayat"]=f2
                        data_dict["village"] = f3
                        data_dict["party_position"]=party_position
                        try:
                            form=Party.objects.get(name=data_dict['name'] , father_name=data_dict['father_name'] ,dob=data_dict['dob'],phone_number=data_dict['phone_number'],booth_number=data_dict['booth_number'] ,mandal=data_dict['mandal'] ,gram_panchayat=data_dict['gram_panchayat'],village=data_dict['village'],party_position=data_dict['party_position'])
                            inf="Data already exist"
                            updated.append(inf)
                        except:
                            form = Party(name=data_dict['name'] , father_name=data_dict['father_name'] ,dob=data_dict['dob'],phone_number=data_dict['phone_number'],booth_number=data_dict['booth_number'] ,mandal=data_dict['mandal'] ,gram_panchayat=data_dict['gram_panchayat'],village=data_dict['village'],party_position=data_dict['party_position'])
                            try:
                                form.save()
                                inf="Data saved"
                                updated.append(inf)
                            except:
                                inf="Got unexpected error at line number:-->"+str(lines.index(line)+2)
                                updated.append(inf)
                    else:
                        inf="<-------New information recieved please update the information and import it again------->"
                        updated.append(inf)
                except:
                    inf="Got data which is incorrect check DOB,Phone Number at line number:-->"+str(lines.index(line)+1)
                    updated.append(inf)
        inf="<-------Process Succressfully created------->"
        updated.append(inf)     
               
        context = {
                    "error_message":updated
            }
        return render(request, 'cm/partyimport.html', context)

def partyexport(request,p_ids):
    data=p_ids
    object_list=Party.objects.all()
    if(data!="" and data!=None and data!="None"):
        data=eval(data)
        object_list=[]
        for i in data:
            object_list.append(Party.objects.get(id=i))
        print(object_list)
    print(object_list)
    #dat=json.loads(request.GET.get('list'))
    #print(type(dat))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PartyData.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Father Name', 'DOB', 'Phone Number','Booth number','Mandal','Gram panchayat','Village','Party position'])
    '''
    party_resource = PartyResource()
    dataset = party_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response'''
    for i in object_list:
        data=[i.name,i.father_name,i.dob,i.phone_number,i.booth_number,i.mandal.mandal,i.gram_panchayat.gp,i.village.village,i.party_position.party_position]
        writer.writerow(data)
    return response

def partycomp(request):
    object_list=Party.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PartyData.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Father Name', 'DOB', 'Phone Number','Booth number','Mandal','Gram panchayat','Village','Party position'])
    '''
    party_resource = PartyResource()
    dataset = party_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response'''
    for i in object_list:
        data=[i.name,i.father_name,i.dob,i.phone_number,i.booth_number,i.mandal.mandal,i.gram_panchayat.gp,i.village.village,i.party_position.party_position]
        writer.writerow(data)
    return response

    
def exportTelgue(request):
    translator = Translator()
    object_list=Party.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PartyData.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Father Name', 'DOB', 'Phone Number','Booth number','Mandal','Gram panchayat','Village','Party position'])
    for i in object_list:
        data=[translator.translate(i.name,dest='te').text,translator.translate(i.father_name,dest='te'),i.dob,i.phone_number,i.booth_number,translator.translate(i.mandal.mandal,dest='te'),translator.translate(i.gram_panchayat.gp,dest='te'),translator.translate(i.village.village,dest='te'),translator.translate(i.party_position.party_position,dest='te')]
        writer.writerow(data)
    return response
