from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import ConstencyForm ,PartyForm,FilterForm,Partypos
from .models import Constency,Mandal,GramPanchayat,Village,Party,PartyFilter,PartyPosition,Smsapi
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
import datetime
from django.http import HttpResponse
import csv
from .resource import PartyResource
import codecs
from django.utils.encoding import  smart_text
from django.conf import settings
import os
import xlwt
import xlrd
from datetime import datetime
import requests as req
import urllib.parse as u1
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



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

@login_required
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


@login_required
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

@login_required
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
       

@login_required
def PartyCreateView(request):
    form = PartyForm(request.POST or None)
    if request.method == 'POST':
        try:
            profile=request.FILES['profile']
        except:
            profile=None
    if form.is_valid():
        party=form.save(commit=False)
        name=party.name
        party.profile=profile
        phone_number=party.phone_number
        try:
            obj=Party.objects.get(phone_number=phone_number)
            if obj:
                context={
                    'error_message':'Data already exist',
                    'form':form
                }
                return render(request, 'cm/partycreateview.html', context)
        except:
            party.save()
            context={
                'error_message':'Data Saved',
                'form':form
            }
            return render(request, 'cm/partycreateview.html', {'form':PartyForm()})
    else:
        return render(request, 'cm/partycreateview.html',{'form':form})
        

    #template_name=""
    #form_class=PartyForm
    
    #success_url=reverse_lazy('cm:person_add')

def load_gram_panchayat(request):
    mandal_id=request.GET.get('mandal')
    gram_panchayat=GramPanchayat.objects.filter(mandal_id=mandal_id)
    return render(request,'cm/dd.html',{'gram_panchayat':gram_panchayat})

def load_village(request):
    gp_id=request.GET.get('gram_panchayat')
    village =Village.objects.filter(gp_id=gp_id)
    return render(request,'cm/vv.html',{'village':village})



@method_decorator(login_required, name='dispatch')
class PartyDatabase(ListView):
    model=Party
    template_name="cm/tables.html"


@method_decorator(login_required, name='dispatch')
class PartyUpdateView(UpdateView):
    model=Party
    template_name="cm/partyupdateview.html"
    form_class=PartyForm
    success_url=reverse_lazy('cm:partydata')
    context_object_name='form'
    def get_context_data(self,**kwargs):
        context=super(PartyUpdateView,self).get_context_data(**kwargs)
        context['pk']=self.object.id
        return context

@method_decorator(login_required, name='dispatch')
class PartyDelete(DeleteView):
    model=Party
    success_url=reverse_lazy('cm:partydata')

@method_decorator(login_required, name='dispatch')
class partypositionC(SuccessMessageMixin,CreateView):
    model=PartyPosition
    template_name="cm/partyposition.html"
    form_class=Partypos
    success_url=reverse_lazy('cm:partyposC')
    context_object_name='form'
    success_message = "Party position was successfully created"


object_list=Party.objects.all()

@login_required
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


@login_required
def partyimport(request):
    data={}
    if "GET" == request.method:
        return render(request, "cm/partyimport.html", data)
    else:
        csv_file = request.FILES['csv_file']
        sup_format=['.xlsx','.csv']

        if not (csv_file.name.endswith('.xlsx') or csv_file.name.endswith('.csv') or csv_file.name.endswith('.xls')):
            context={"error_message":["File is not csv nor xlsx type"]}
            return render(request, "cm/partyimport.html", context)
        if csv_file.multiple_chunks():
            context={"error_message":["Uploaded file is too big."]}
            return render(request, "cm/partyimport.html", context)
        #CSV file error handle
        if(csv_file.name.endswith('.csv')):
            file_data = csv_file.read().decode("utf-8")
            print(file_data)
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
                                form=Party.objects.get(phone_number=data_dict['phone_number'])
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
        elif(csv_file.name.endswith('.xlsx') or csv_file.name.endswith('.xls')):
            book = xlrd.open_workbook(file_contents=csv_file.read())
            sheet = book.sheet_by_index(0)
            data=[]
            p=[]
            for i in range(1,sheet.nrows):
                data.append(sheet.row_values(i))
            
            for i in data:
                i[2] = datetime(*xlrd.xldate_as_tuple(i[2], 0))
                i[2]=i[2].strftime('%d/%m/%Y')
                   
                i[3]=str(int(i[3]))
                i[4]=str(int(i[4]))
            lines=data
            
            updated=[]
            for line in data:                        
                fields = line 
                if('' in fields):
                    fields.remove('')
                if(len(fields)==9):
                    print("I am here")
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
                                form=Party.objects.get(phone_number=data_dict['phone_number'])
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
                            "error_message":updated,
                }
            return render(request, 'cm/partyimport.html', context)
        
        
@login_required
def partyexport(request,p_ids):
    data=p_ids
    object_list=Party.objects.all()
    if(data!="" and data!=None and data!="None"):
        data=eval(data)
        object_list=[]
        for i in data:
            object_list.append(Party.objects.get(id=i))
      
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PartyData.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Partydata')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'
    columns = ['Name', 'Father Name', 'DOB', 'Phone Number','Booth number','Mandal','Gram panchayat','Village','Party position']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    #writer = csv.writer(response)
    #writer.writerow(['Name', 'Father Name', 'DOB', 'Phone Number','Booth number','Mandal','Gram panchayat','Village','Party position'])
    font_style = xlwt.XFStyle()
    rows=object_list
    for i in rows:
        row=[i.name,i.father_name,i.dob,i.phone_number,i.booth_number,i.mandal.mandal,i.gram_panchayat.gp,i.village.village,i.party_position.party_position]
        row_num += 1
        for col_num in range(len(row)):
            if(col_num==2):
                ws.write(row_num, col_num, row[col_num], date_format)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

    #for i in object_list:
     #   data=[i.name,i.father_name,i.dob,i.phone_number,i.booth_number,i.mandal.mandal,i.gram_panchayat.gp,i.village.village,i.party_position.party_position]
      #  writer.writerow(data)
    #return response


@login_required
def partycomp(request):
    object_list=Party.objects.all()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PartyData.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Partydata')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'
    columns = ['Name', 'Father Name', 'DOB', 'Phone Number','Booth number','Mandal','Gram panchayat','Village','Party position']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows=object_list
    for i in rows:
        row=[i.name,i.father_name,i.dob,i.phone_number,i.booth_number,i.mandal.mandal,i.gram_panchayat.gp,i.village.village,i.party_position.party_position]
        row_num += 1
        for col_num in range(len(row)):
            if(col_num==2):
                ws.write(row_num, col_num, row[col_num], date_format)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def get_num(object_list):
    num=''
    for i in object_list:
        num=num+","+i.phone_number
    return(num)


@login_required
def sms(request):
    form = FilterForm(request.POST or None)
    if("filter" in request.POST):
        form = FilterForm(request.POST or None)
        if form.is_valid():
            m1=request.POST.get('mandal')
            m2=request.POST.get('gram_panchayat')
            m3=request.POST.get('village')
            m4=request.POST.get('party_position')
            #object_list=Party.objects.filter(mandal_id=m1,gram_panchayat_id=m2,village_id=m3,party_position_id=m4)
            if(m1=='' and m2=='' and m3=='' and m4==''):
                context={
                "error_message":"Please choose some option",
                "form":form, 
                "object_list":Party.objects.all(),
                }
                return render(request, 'cm/smsmgt.html', context)
            
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
            num=get_num(object_list) 
            context={
                "object_list":Party.objects.all(),
                "error_message":"You Activated the filter",
                "form":form,
                "num":num
            }
            return render(request, 'cm/smsmgt.html', context)
        else:
            context={
                "object_list":Party.objects.all(),
                "form":form ,
            }
            return render(request, 'cm/smsmgt.html', context)
        #return render(request, 'cm/smsmgt.html', context)
    elif('sms' in request.POST):
        mob=request.POST.get('mobnos')
        msg=request.POST.get('msg')
        msg=u1.quote_plus(msg)
        print(msg)
        mob=mob.rstrip('\r').split(',')
        null=mob.count('')
        for i in range(null):
            mob.remove('')
        u_mob=[]
        updt=[]
        for i in mob:
            if(i not in u_mob):
                if(i.isdigit() and len(i)==10):
                    u_mob.append(i)
                else:
                    updt.append("Please give valid phone number :-"+str(i))
        count=len(u_mob)
        sms_api=Smsapi.objects.all()
        sms_api=str(sms_api[0])
        sms_api=sms_api.replace('[MESSAGE]',msg)
        s_count=0
        send_msg=''
        not_send=[]
        for i in u_mob:
            sms_api=sms_api.replace('[MOBNO]',i)
            send=req.get(sms_api)
            send_msg=send.content.decode()
            sms_api=sms_api.replace(i,'[MOBNO]')
            print(send_msg)
            if("SHOOT" in send_msg):
                s_count=s_count+1
            else:
                not_send.append(i)
        if(s_count!=0):
            send_msg='Messages sent successfully  '+str(s_count)+"/"+str(count)
        if(len(not_send)>0):
            send_msg=send_msg+"\n"+"Message cannot be sent to -->"+str(not_send)
        context={
            'object_list':Party.objects.all(),
            'form':form,
            'success_msg':send_msg,
            'valid':updt
        }
        return render(request, 'cm/smsmgt.html', context)
    else:
        context={
                "object_list":Party.objects.all(),
                "form":form ,
        }
        return render(request, 'cm/smsmgt.html', context)
        

@login_required        
def sample_download(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PartyData.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Partydata')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'
    columns = ['Name', 'Father Name', 'DOB', 'Phone Number','Booth number','Mandal','Gram panchayat','Village','Party position']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    wb.save(response)
    return response


@method_decorator(login_required, name='dispatch')
class PartyDatabase_photo(ListView):
    model=Party
    template_name="cm/photomanagement.html"


@login_required
def photo_manage(request):
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
            return render(request, 'cm/photomanagement.html', context)
        
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
        return render(request, 'cm/photomanagement.html', context)
    else:
        context={
            "object_list":Party.objects.all(),
            "form":form ,
            "p_ids":"None"
        }
        return render(request, 'cm/photomanagement.html', context)