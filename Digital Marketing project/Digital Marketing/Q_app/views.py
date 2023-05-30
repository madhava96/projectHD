from django.shortcuts import render,redirect
from .models import clientdetails,requirements,user_report,logindetails
from django.db.models import Q

from django.shortcuts import render,redirect
from django.contrib import messages
#from .models import requirements,clientdata,user_report

from django.core import serializers
import json

import os
import MySQLdb as sql
import random
import smtplib
from django.http import HttpRequest

#mysql connection function
def sqlconn():
    conn = sql.connect(user='dmuser',passwd='admin',db='marketing',host="192.168.30.93")
    cur = conn.cursor()
    return cur,conn


# Create your views here.
#-------------------------------------------------login page ------------------------(fixed by sky)
#login super admin ,user and client

'''when client will login its id and name stroing below'''
#clientid='' 
clientname=''


def login(request):
    global clientid, clientname
    cur,conn = sqlconn()
    if request.method == 'GET':
        return render(request,'login.html')
    else: #login authentication
        global username
        username=request.POST.get('username')
        password=request.POST.get('password')
        uname=logindetails.objects.filter(username=username)
        pwd=logindetails.objects.filter(password=password)
        if uname and pwd:
            dsig = logindetails.objects.filter(username=username)
            for i in dsig:
                dsg=i.role 
                if dsg =='superadmin':
                    return render(request,'SAdmin_Homepage.html') 
                elif dsg =='user':
                    return redirect(userhomepage)
                else:
                    messages.success(request,'Invalid details!')
                    return render(request,'login.html')
        else:
            uname=clientdetails.objects.filter(username=username)
            #pwd = uname.values()[0]['password']
            q = "select cast(aes_decrypt(password, 'pass') as char)as password from q_app_clientdetails where username = '{}'".format(username)
            cur.execute(q)
            pwd = cur.fetchone()
            if pwd  is not None:
                pwd = pwd[0]
            #print(pwd)
            if uname and (pwd==password):
                dsig = clientdetails.objects.filter(username=username)
                #print(dsig)
                for i in dsig:
                    dsg=i.role 
                    if dsg =='client':
                        print(i.id)
                        clientid = i.id
                        cl_id = 'select id from q_app_requirements where deptid_id = {}'.format(clientid)
                        cur.execute(cl_id)
                        clientid = cur.fetchone()[0]
                        conn.commit()
                        q = "select distinct campaign_name from  q_app_user_report where clientname = '{}'".format(i.clientname)
                        cur.execute(q)
                        campaigns = list(cur.fetchall())
                        #print(campaigns[0][0],campaigns[0])
                        #campaigns=user_report.objects.filter(clientid_id = i.id).distinct()
                        clientname = i.clientname
                        campaign = user_report.objects.filter(campaign_name=campaigns[0][0]).order_by('date')
                        #report,cost= statics(i.id)
                        report,dates,no_impre,no_clicks = statics(campaigns[0][0])
                        return render(request, 'campaign.html',{'campaign':campaign,'campaigns':campaigns,'client':clientname,'data':report,'dates':dates,'impr':no_impre,'clicks':no_clicks, 'camp':campaigns[0][0]})


                        #return render(request, 'campaign.html',{'campaigns':campaigns,'client':clientname})#,'data':report,'cost':cost,'clicks':0})
            else:
                messages.success(request,'Invalid details!')
                return render(request,'login.html')
        
#--------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------client page -------------------------------------------------(fixed by sky)
# clients can see campaigns
def statics(camp):
    print(camp)
    cur,conn = sqlconn()
    q = "select * from  q_app_user_report where campaign_name = '{}' order by date".format(camp)
    cur.execute(q)
    conn.commit()
    data =  list(cur.fetchall())
    sum_impressions = 0
    sum_clicks = 0
    total_cost_impr = 0
    total_cost_click = 0
    total_cost_per_day = 0
    dates= []
    no_impre =[]
    no_clicks =[]
    for i in data:
        dates.append(i[3])
        no_impre.append(i[4])
        no_clicks.append(i[5])
        i=list(i)[4:]
        sum_impressions += i[0]
        sum_clicks +=i[1]
        total_cost_impr +=i[4]
        total_cost_click +=i[5]
        total_cost_per_day +=i[6]
    report=[sum_impressions,sum_clicks,total_cost_per_day]
    return (report, dates, no_impre,no_clicks)
    

def campaign_details(request):
    print(request)
    global clientid
    #print('client',clientid)
    cur,conn = sqlconn()
    print(clientid)
    q = "select distinct campaign_name from  q_app_user_report where clientname = '{}'".format(clientname)
    cur.execute(q)
    campaigns = list(cur.fetchall())
    print(campaigns)
    conn.commit()
    #q = 'select no_of_impressions, no_of_clicks campaign_name from  q_app_user_report where clientid_id = {}'.format(clientid)
    #cur.execute(q)
    #print(statics(clientid))
    #labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    if request.method == 'POST':
        selected_campaign = request.POST.get('campaign_name')
        #print(selected_campaign)
        campaign = user_report.objects.filter(campaign_name=selected_campaign).order_by('date')
        #campaigns=user_report.objects.filter(clientid_id = clientid).distinct('campaign_name')
        #context = {'campaign': campaign,'campaigns':campaigns,'client':clientname}
        report,dates,no_impre,no_clicks = statics(selected_campaign)
        #print(report,cost,dates,no_impre)
        context = {'campaign': campaign,'campaigns':campaigns,'client':clientname,'data':report,'dates':dates,'impr':no_impre,'clicks':no_clicks,'camp':selected_campaign}
        return render(request, 'campaign.html', context)
    else:
        #print(campaigns)
        #report,cost = statics(clientid)
        #campaigns=user_report.objects.filter(clientid_id = clientid).distinct('campaign_name')
        return render(request, 'campaign.html',{'campaigns':campaigns,'client':clientname})
        #return render(request, 'campaign.html',{'campaigns':campaigns,'client':clientname})#'data':report,'cost':cost,'dates':dates,'impr':no_impre,'clicks':0})
    
#--------------------------------------------------------------------------------------------------------------------------------
# super admin homepage
def homepage(request):
    return render(request,'SAdmin_homepage.html')
# user home page
def userhomepage(request):
    return render(request,'User_Homepage.html')

# client form
def upload_image(request):
    if request.method=='GET':
        dat=clientdetails.objects.all().values()  #displaying the values that are before saved
        return render(request,'SAdmin_ClientDetails.html',{'dat':dat}) 

    elif request.method=='POST':
        clientname=request.POST['clientname']
        if clientdetails.objects.filter(clientname=clientname).exists(): # it checks client name is already registered or not
            messages.error(request,"Client Name already registered !")  
            return render(request,'SAdmin_ClientDetails.html')
        else:
            data = dict()
            if "GET" == request.method:
                return render(request, 'SAdmin_ClientDetails.html', data)
            # process POST request
            files=request.FILES  # multivalued dict
            clientname=request.POST.get('clientname')
        
            username=request.POST.get('username')
            password=request.POST.get('password')
            email= request.POST.get('email')
            date=request.POST.get('date')
            image = files.get("image")
            if image is None:
                image = 'uploads/dummy.png'
            #print(image)
            role = 'client'
            instance = clientdetails()
            instance.clientname = clientname
        
            instance.username = username
            instance.password = instance._enc(password)#it will call property in models
            instance.email = email
            instance.date = date
            instance.image = image
            instance.role = role
            instance.save()
            
            #p=ImageModel.objects.all()
            messages.success(request,"Form Submitted Successfully")
            return render(request, 'SAdmin_ClientDetails.html')

# view campaign requriements data
def taskdata(request):
    td=requirements.objects.all()
    return render(request,'SAdmin_Taskdata.html',{'td':td})

#----------------------------------------------task requirment page for superadmin ---------------------(fixed by sky)

def taskcreation(request):
    
    cur,conn = sqlconn()
    if request.method=='GET':
        print(request)
        #people = clientdetails.objects.all()
        q = 'select id ,clientname from  q_app_clientdetails'
        cur.execute(q)
        people = list(cur.fetchall())
        #print(people,type(people))
        return render(request,'taskcreation.html',{'people': people})
    
    elif request.method=='POST':
        people=requirements.objects.all().values()
        campaign_name=request.POST['campaign_name']
        #print(people)
            
        if requirements.objects.filter(campaign_name=campaign_name).exists(): # it checks client name is already registered or not
            messages.error(request,"Campaign Name already registered !")  
            return render(request,'taskcreation.html',{'people': people})
        
   
        else:
            name=request.POST.get('name')  #its having id and client name
            name = name.replace("(", "")
            name = name.replace(")", "")
            name = name.replace(",", " ")
            name = name.replace("'", "")
            name = name.replace("'", "")
            name = name.split()
            print(name,type(name))
            requirements(
                name=name[1],
                campaign_name=request.POST.get('campaign_name'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                planned_impressions=request.POST.get('planned_impressions'),
                planned_cpm=request.POST.get('planned_cpm'),
                planned_cpc=request.POST.get('planned_cpc'),
                planned_cost=request.POST.get('planned_cost'),
                deptid_id=name[0]
            ).save()
            messages.success(request,"Form Submitted Successfully")
            #people = clientdetails.objects.all()
            q = 'select id ,clientname from  q_app_clientdetails'
            cur.execute(q)
            people = list(cur.fetchall())
            conn.commit()
            return render(request,'taskcreation.html',{'people': people})

#------------------------------------------------------------------------------------------------------------------


def taskcreation_user(request):
    
    cur,conn = sqlconn()
    if request.method=='GET':
        #people = clientdetails.objects.all()
        q = 'select id ,clientname from  q_app_clientdetails'
        cur.execute(q)
        people = list(cur.fetchall())
        print(people,type(people))
        return render(request,'taskcreation_user.html',{'people': people})
    
    elif request.method=='POST':
        people=requirements.objects.all().values()
        campaign_name=request.POST['campaign_name']
        #print(people)
            
        if requirements.objects.filter(campaign_name=campaign_name).exists(): # it checks client name is already registered or not
            messages.error(request,"Campaign Name already registered !")  
            return render(request,'taskcreation_user.html',{'people': people})
        
   
        else:
            name=request.POST.get('name')  #its having id and client name
            name = name.replace("(", "")
            name = name.replace(")", "")
            name = name.replace(",", " ")
            name = name.replace("'", "")
            name = name.replace("'", "")
            name = name.split()
            #print(name,type(name))
            requirements(
                name=name[1],
                campaign_name=request.POST.get('campaign_name'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                planned_impressions=request.POST.get('planned_impressions'),
                planned_cpm=request.POST.get('planned_cpm'),
                planned_cpc=request.POST.get('planned_cpc'),
                planned_cost=request.POST.get('planned_cost'),
                deptid_id=name[0]
            ).save()
            messages.success(request,"Form Submitted Successfully")
            #people = clientdetails.objects.all()
            q = 'select id ,clientname from  q_app_clientdetails'
            cur.execute(q)
            people = list(cur.fetchall())
            conn.commit()
            return render(request,'taskcreation_user.html',{'people': people})


# delete campaign req data 
def delete(request, id):
    td=requirements.objects.get(id=id)
    td.delete()
    return redirect("/taskdata")

# edit campaign req data
def edit(request, id):

    td=requirements.objects.get(id=id)
    return render(request,'edittaskdata.html',{'td':td})

#  campaign req data
def update(request, id):
    
    #people = Person.objects.get(id=id)
    #name=request.POST.get('name'),
    campaign_name=request.POST.get('campaign_name')
    start_date=request.POST.get('start_date')
    end_date=request.POST.get('end_date')
    planned_impressions=request.POST.get('planned_impressions')
    planned_cpm=request.POST.get('planned_cpm')
    planned_cpc=request.POST.get('planned_cpc')
    planned_cost=request.POST.get('planned_cost')
    deptid_id = request.POST.get('deptid_id')
    td=requirements.objects.get(id=id)

    #td.name=name
    
    td.campaign_name=campaign_name
    td.start_date=start_date
    td.end_date=end_date
    td.planned_impressions=planned_impressions
    td.planned_cpm=planned_cpm
    td.planned_cpc=planned_cpc
    td.planned_cost=planned_cost
    td.deptid_id=deptid_id

    td.save()
    
    return redirect(taskdata) 
    #return render({'people': people})       
'''
def u_report(request):
    if request.method=='GET':
        people = clientdetails.objects.all()
        rd=user_report.objects.all()
        return render(request,'user_report.html',{'people': people},{'rd':rd})
    else:
        user_report(
            name=request.POST.get('name'),
            campaign_name=request.POST.get('campaign_name'),
            date=request.POST.get('date'),
            no_of_impressions=request.POST.get('no_of_impressions'),
            no_of_clicks=request.POST.get('no_of_clicks'),
            cost_per_impressions=request.POST.get('cost_per_impressions'),
            cost_per_click=request.POST.get('cost_per_click'),
            total_cost_per_impressions=request.POST.get('total_cost_per_impressions'),
            total_cost_per_click=request.POST.get('total_cost_per_click'),
            cost_per_day=request.POST.get('cost_per_day')

        ).save()
        people = clientdetails.objects.all()
        return render(request,'user_report.html',{'people': people})
'''



#-----------------------------------Report Details page----------------------------------(fixed by sky)
import datetime
def status(x):
    #print(x)
    x = list(x)
    date = str(datetime.date.today())
    stdate = x[-2]
    enddate = x[-1]
    #print(stdate,enddate,type(stdate))
    if date <=enddate and date >= stdate :
        status = 'Running'
    elif date > enddate and date >= stdate:
        status = 'Closed'
    else:
        status = 'Pending'
    x = x[:-2]
    x.append(status)
    return x
#------------------------------------------report details page --------------------------------
from django.http import JsonResponse

def fetch_dependent_options(request):
    parent_value = request.GET.get('parentValue')
    dependent_options = requirements.objects.filter(deptid=parent_value).values('campaign_name')
    #print(dependent_options)

    return JsonResponse(list(dependent_options), safe=False)

def fetch_data(request):
    print(request.GET.get('parentValue'))
    parentValue = request.GET.get('parentValue')
    dependValue = request.GET.get('dependValue')
    print(request.GET.get('dependValue'))
    cur,conn = sqlconn()
    q=''
    if parentValue == 'all' and dependValue is None:
        q = 'select q_app_user_report.id,q_app_user_report.clientname,  q_app_user_report.campaign_name,date, no_of_impressions,no_of_clicks,cost_per_impressions,cost_per_click,total_cost_per_impressions,total_cost_per_click,cost_per_day,start_date,end_date from q_app_user_report inner join q_app_requirements on clientid_id = q_app_requirements.id where q_app_user_report.campaign_name = q_app_requirements.campaign_name order by date desc;'
    elif parentValue != 'all' and dependValue=='':
        q1="select campaign_name from q_app_requirements where deptid_id = {}".format(parentValue)
        cur.execute(q1)
        res = cur.fetchone()[0]
        #print(res)
        q = "select q_app_user_report.id,q_app_user_report.clientname,  q_app_user_report.campaign_name,date, no_of_impressions,no_of_clicks,cost_per_impressions,cost_per_click,total_cost_per_impressions,total_cost_per_click,cost_per_day,start_date,end_date from q_app_user_report inner join q_app_requirements on clientid_id = q_app_requirements.id where q_app_user_report.campaign_name = q_app_requirements.campaign_name and q_app_requirements.deptid_id ={} and q_app_requirements.campaign_name='{}' order by date desc;".format(parentValue,res)
    else:
        q = "select q_app_user_report.id,q_app_user_report.clientname,  q_app_user_report.campaign_name,date, no_of_impressions,no_of_clicks,cost_per_impressions,cost_per_click,total_cost_per_impressions,total_cost_per_click,cost_per_day,start_date,end_date from q_app_user_report inner join q_app_requirements on clientid_id = q_app_requirements.id where q_app_user_report.campaign_name = q_app_requirements.campaign_name and q_app_requirements.deptid_id ={} and q_app_requirements.campaign_name='{}' order by date desc;".format(parentValue,dependValue)
        
    cur.execute(q)
    data = list(cur.fetchall())
    conn.commit()
    rd = list(map(status,data))
    print(rd)
    return  JsonResponse(rd, safe=False)


def reportdata(request):
    print(request)
    cur,conn = sqlconn()
    q1 = 'select DISTINCT deptid_id ,clientname from q_app_clientdetails inner join q_app_requirements on q_app_clientdetails.id =  deptid_id;'
    cur.execute(q1)
    people = list(cur.fetchall()) 
    empcontext = requirements.objects.all()    
    #context={'people':people,'empcontext':empcontext}
    if request.method=="POST":
        print(request)
        datef=request.POST.get("datef")
        datet=request.POST.get("datet")
        parentValue = request.POST.get('parentValue')
        dependValue = request.POST.get('dependValue')
        print(parentValue,dependValue)
        print(datef,datet)
        if datef is not None and datet is not None:
            q="select q_app_user_report.id,q_app_user_report.clientname,  q_app_user_report.campaign_name,date, no_of_impressions,no_of_clicks,cost_per_impressions,cost_per_click,total_cost_per_impressions,total_cost_per_click,cost_per_day,start_date,end_date from q_app_user_report inner join q_app_requirements on clientid_id = q_app_requirements.id where q_app_user_report.campaign_name = q_app_requirements.campaign_name and(date >= '{}' and date <='{}');".format(datef,datet)
        #queryset = user_report.objects.filter(date__range=[datef, datet])
        else:
            if parentValue == 'all' and dependValue is None:
                q = 'select q_app_user_report.id,q_app_user_report.clientname,  q_app_user_report.campaign_name,date, no_of_impressions,no_of_clicks,cost_per_impressions,cost_per_click,total_cost_per_impressions,total_cost_per_click,cost_per_day,start_date,end_date from q_app_user_report inner join q_app_requirements on clientid_id = q_app_requirements.id where q_app_user_report.campaign_name = q_app_requirements.campaign_name order by date desc;'
            elif parentValue != 'all' and dependValue=='':
                q1="select campaign_name from q_app_requirements where deptid_id = {}".format(parentValue)
                cur.execute(q1)
                res = cur.fetchone()[0]
                #print(res)
                q = "select q_app_user_report.id,q_app_user_report.clientname,  q_app_user_report.campaign_name,date, no_of_impressions,no_of_clicks,cost_per_impressions,cost_per_click,total_cost_per_impressions,total_cost_per_click,cost_per_day,start_date,end_date from q_app_user_report inner join q_app_requirements on clientid_id = q_app_requirements.id where q_app_user_report.campaign_name = q_app_requirements.campaign_name and q_app_requirements.deptid_id ={} and q_app_requirements.campaign_name='{}' order by date desc;".format(parentValue,res)
            else:
                q = "select q_app_user_report.id,q_app_user_report.clientname,  q_app_user_report.campaign_name,date, no_of_impressions,no_of_clicks,cost_per_impressions,cost_per_click,total_cost_per_impressions,total_cost_per_click,cost_per_day,start_date,end_date from q_app_user_report inner join q_app_requirements on clientid_id = q_app_requirements.id where q_app_user_report.campaign_name = q_app_requirements.campaign_name and q_app_requirements.deptid_id ={} and q_app_requirements.campaign_name='{}' order by date desc;".format(parentValue,dependValue)
                
        cur.execute(q)
        data = list(cur.fetchall())
        conn.commit()
        rd = list(map(status,data))
        print(rd)
        #rd=user_report.objects.all()
        #print(queryset)
        #return render(request,'searchresult.html',{'queryset':queryset})
        #return render(request,'SAdmin_Reportdata.html',{'rd':rd})
        #return render(request,'sky.html',{'people':people,'empcontext':empcontext})
        return render(request,'SAdmin_Reportdata.html',{'rd':rd,'people':people,'empcontext':empcontext})
    else:
        
        q = 'select q_app_user_report.id,q_app_user_report.clientname,  q_app_user_report.campaign_name,date, no_of_impressions,no_of_clicks,cost_per_impressions,cost_per_click,total_cost_per_impressions,total_cost_per_click,cost_per_day,start_date,end_date from q_app_user_report inner join q_app_requirements on clientid_id = q_app_requirements.id where q_app_user_report.campaign_name = q_app_requirements.campaign_name order by date desc;'
        cur.execute(q)
        data = list(cur.fetchall())
        conn.commit()
        rd = list(map(status,data))
        return render(request,'SAdmin_Reportdata.html',{'rd':rd,'people':people,'empcontext':empcontext})
        #return render(request,'sky.html',{'rd':rd,'people':people,'empcontext':str(list(empcontext.values()))})


#------------------------------------------------------------------------------------------



def delete_report(request, id):
    rd=user_report.objects.get(id=id)
    rd.delete()
    return redirect("/reportdata")
#-------------------edit report page -----------------------
def edit_report(request, id):    
    rd=user_report.objects.get(id=id)
    return render(request,'editreportdata.html',{'rd':rd})
#------------------------------------------------------------
def update_report(request, id):
    
    #people = Person.objects.get(id=id)
    #name=request.POST.get('name'),
    date=request.POST.get('date')
    no_of_impressions=request.POST.get('no_of_impressions')
    no_of_clicks=request.POST.get('no_of_clicks')
    cost_per_impressions=request.POST.get('cost_per_impressions')
    cost_per_click=request.POST.get('cost_per_click')
    total_cost_per_impressions=request.POST.get('total_cost_per_impressions')
    total_cost_per_click=request.POST.get('total_cost_per_click')
    cost_per_day=request.POST.get('cost_per_day')
    rd=user_report.objects.get(id=id)

    #td.name=name
    rd.date=date
    rd.no_of_impressions=no_of_impressions
    rd.no_of_clicks=no_of_clicks
    rd.cost_per_impressions=cost_per_impressions
    rd.cost_per_click=cost_per_click
    rd.total_cost_per_impressions=total_cost_per_impressions
    rd.total_cost_per_click=total_cost_per_click
    rd.cost_per_day=cost_per_day

    rd.save()
    return redirect(reportdata) 
    return render({'people': people})




def viewclientdetails(request):
    people=clientdetails.objects.all()
    #image=clientdetails.objects
    return render(request,'SAdmin_ViewClientDetails.html',{'people':people})


def delete_client(request, id):
    people=clientdetails.objects.get(id=id)
    people.delete()
    return redirect("/viewclientdetails")
'''
def edit_client(request, id):

    people=clientdetails.objects.get(id=id)
    return render(request,'editclientdata.html',{'people':people})
'''
def edit_client1(request, id):

    people=clientdetails.objects.get(id=id)
    return render(request,'edit3.html',{'people':people})

def update_client(request, id):
    
    people=clientdetails.objects.get(id=id)
    if request.method == "POST":
        print(request.FILES)
        if len(request.FILES) != 0:
            people.image = request.FILES['image']
    
        people.email = request.POST.get('email')
        people.date=request.POST.get('date')
        people.save()
        #messages.success(request, "Product Updated Successfully")
        return redirect(viewclientdetails)    

    context = {'people':people}
    return render(request, 'SAdmin_ViewClientDetails.html', context)

'''
def newlogin(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else: #login authentication
        global username
        username=request.POST.get('username')
        password=request.POST.get('password')
        uname=logindetails.objects.filter(username=username)
        pwd=logindetails.objects.filter(password=password)

        if uname and pwd:
            dsig = logindetails.objects.filter(username=username)
            for i in dsig:
                dsg=i.role 
                if dsg =='superadmin':
                    return render(request,'SAdmin_Homepage.html') 
                else:
                    return redirect(userhomepage)

                
                
        else:
            #messages.success(request,'Invalid details!')
            return render(request,'login.html')

'''
'''
def forgotpassword(request):
    if request.method == 'POST':
        form1 = fpForm(request.POST)
        if form1.is_valid():
            # Create instances of both models

            #table1_instance = logindetails(password=form1.cleaned_data['password'])
            table2_instance = forgot_password(password=form1.cleaned_data['password'], confirm_password=form1.cleaned_data['confirm_password'])
            
            
            # Save both instances
            #table1_instance.save()
            table2_instance.save()
            
            mail=request.POST.get('mail')
            password=request.POST.get('password')


            p=logindetails.objects.filter(mail=mail)
            if p:
                p.update(password=password)
                e="Password Changed Successfully"
                # Redirect to success page
                return render(request, 'forgotpassword.html',{'e':e})
    else:
        form1 = fpForm()
    return render(request, 'forgotpassword.html', {'form1': form1})

'''
#----------------------------forgotpasswordpage----------------------------------------------------------------------
def forgotpassword(request):
    otp =''
    if request.method == 'POST':
        user = request.POST.get('username')
        email = request.POST.get('email')
        print(user,email)
        if clientdetails.objects.filter(Q(username=user)& Q(email=email)).exists():
            data = clientdetails.objects.filter(Q(username=user)& Q(email=email))[0]
            mail = data.email
            id = str(data.id)
            print(id,type(id))
            print('exists',mail)
            from_addr ="adandge805@gmail.com"
            password = "hdyvxcfrrbqfzgqp"
            
            no= str(random.randrange(111111, 999999, 6))
            msg="""
Varification Code for RESET PASSWORD:{}
            """.format(no)
            otp=no+','+id
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(from_addr,password)
            print("Login Successful")
            server.sendmail(from_addr,mail,msg)
            print(msg)
            print("OTP Succefully Sended...")
            server.quit()
            messages.success(request,"OTP Succefully Sended...")
            return render(request, 'validate.html',{'otp':otp,'disotp':'block','disreset':'none'})#'dispreset':'none','disp':'block'})
        else:
            print('not exists')
            messages.error(request,"Enter Valid Details !")
            return render(request, 'forgotpassword.html')

    return render(request, 'forgotpassword.html')
#--------------------------------------------------------------------------------------------------------------------------


#---------------------validate otp and  reset the password --------------------------------------------------------------
def validate(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        data = request.POST.get('conf_otp')
        if otp is not None and data is not None:
            print(otp,data)
            data = data.split(',')
            conf_otp = data[0]
            if otp==conf_otp:
                messages.success(request,"Varification Succefully Done")
                return render(request, 'validate.html',{'otp':request.POST.get('conf_otp'),'disotp':'none','disreset':'block'})
            else:
                messages.error(request,"Enter Valid Varification Code")
                return render(request, 'validate.html',{'otp':request.POST.get('conf_otp'),'disotp':'block','disreset':'none'})
        else:
            new_pass = request.POST.get('newpass')
            conf_pass = request.POST.get('confpass')
            data = request.POST.get('conf_otp_id')
            print(new_pass,conf_pass)
            id = int(data.split(',')[1])
            #print(id)
            print(new_pass == conf_pass)
            if new_pass == conf_pass:
                cur,conn=sqlconn()
                q="update q_app_clientdetails set password=AES_ENCRYPT('{}','pass') where id = {}".format(new_pass,id)
                cur.execute(q)
                conn.commit()
                messages.success(request,"Password Succefully Changed Log In Now")
                return render(request, 'login.html')
            else:
                return render(request, 'validate.html',{'otp':request.POST.get('conf_otp'),'disotp':'none','disreset':'block'})
#------------------------------------------------------------------------------------------------------------------------------------------            

# def forgotpassword(request):
#     if request.method=="GET":

#         #ld=logind.objects.all()
#         return render(request,'forgotpassword.html')
#     else:

#         forgotpassword(
#            password =request.POST.get('password'),
#            confirmpassword=request.POST.get('confirmpassword')
        

#         ).save()

#         clientdetails(
#             password =request.POST.get('password')
#         ).save()
        
#         # p=logindetails.objects.filter(mail=mail)
#         # if p:
#         #     p.update(password=password)
#         e="Password Changed Successfully"
#         return render(request,'forgotpassword.html',{'e':e})
        
# def u_report(request):
#     if request.method=='GET':
#         people = clientdetails.objects.all()
#         #deptcontext = clientdetails.objects.all()
#         empcontext = requirements.objects.all()    
#         context={'people':people,'empcontext':empcontext}
#         return render(request,'user_report.html',context)

#     elif request.method=='POST':
#         date=request.POST['date']
#         if clientdetails.objects.filter(date=date).exists(): # it checks client name is already registered or not
#             messages.error(request,"Given Date Already Registered !")  
#             return render(request,'SAdmin_ClientDetails.html')

    
#         else:
#             user_report(
#                 clientname=request.POST.get('hiddenclient'),
#                 campaign_name=request.POST.get('hiddencampaign'),
#                 date=request.POST.get('date'),
#                 no_of_impressions=request.POST.get('no_of_impressions'),
#                 no_of_clicks=request.POST.get('no_of_clicks'),
#                 cost_per_impressions=request.POST.get('cost_per_impressions'),
#                 cost_per_click=request.POST.get('cost_per_click'),
#                 total_cost_per_impressions=request.POST.get('total_cost_per_impressions'),
#                 total_cost_per_click=request.POST.get('total_cost_per_click'),
#                 cost_per_day=request.POST.get('cost_per_day')
#             ).save()
#             people = clientdetails.objects.all()
#             #deptcontext = clientdetails.objects.all()
#             empcontext = requirements.objects.all()    
#             context={'people':people,'empcontext':empcontext}
#             messages.success(request,'Form Submitted Successfully')
#             return render(request,'user_report.html',context)

#--------------------------------------------------Report form page---------------------------------------(fixed by sky)
def u_report(request):
    cur,conn= sqlconn()
    
    '''
    if request.method=='GET':
        people = clientdetails.objects.all()
        #deptcontext = clientdetails.objects.all()
        empcontext = requirements.objects.all()    
        context={'people':people,'empcontext':empcontext}
        print(people ,'\n', empcontext)
        return render(request,'user_report.html',context)
    '''
    '''
    if request.method=='GET':
            q1 = 'select DISTINCT deptid_id ,clientname from q_app_clientdetails inner join q_app_requirements on q_app_clientdetails.id =  deptid_id;'
            cur.execute(q1)
            people = list(cur.fetchall())
            #print(people,type(people))
            #q2 = 'select * from  q_app_clientdetails'
            #cur.execute(q2)
            #empcontext = list(cur.fetchall())
            #context={'people':people,'empcontext':empcontext}
            empcontext = requirements.objects.all()    
            context={'people':people,'empcontext':empcontext}
            #print(people ,'\n', empcontext)
            return render(request,'user_report.html',{'people':people,'empcontext':empcontext})
            #return render(request,'user_report.html',{'people':people})
    '''
    q1 = 'select DISTINCT deptid_id ,clientname from q_app_clientdetails inner join q_app_requirements on q_app_clientdetails.id =  deptid_id;'
    cur.execute(q1)
    people = list(cur.fetchall()) 
    empcontext = requirements.objects.all()    
    context={'people':people,'empcontext':empcontext}
    if request.method=='GET':
        #people = clientdetails.objects.all()
        #deptcontext = clientdetails.objects.all()
        
        #print(people ,'\n', empcontext)
        return render(request,'user_report.html',context)
    
    elif request.method=='POST':
        clientname=request.POST.get('hiddenclient')
        campaign_name=request.POST.get('hiddencampaign')
        if clientname == '' or campaign_name == '':
            messages.error(request,'Select Client And Campaign Data')
            return render(request,'user_report.html',context)
        else:
            clientname = clientname.replace("\r\n"," ")
            clientname = clientname.strip()
            campaign_name=campaign_name.replace("\r\n"," ")
            #print(campaign_name)
            campaign_name=campaign_name.strip()
            date=request.POST['date']
            if user_report.objects.filter(Q(date=date) & Q (clientname=clientname) & Q(campaign_name=campaign_name)).exists(): # it checks client name is already registered or not
                q1 = 'select DISTINCT deptid_id ,clientname from q_app_clientdetails inner join q_app_requirements on q_app_clientdetails.id =  deptid_id;'
                cur.execute(q1)
                people = list(cur.fetchall()) 
                #people = clientdetails.objects.all()
                empcontext = requirements.objects.all()    
                context={'people':people,'empcontext':empcontext}
                messages.error(request,"Given Date Already Registered !")  
                return render(request,'user_report.html',context)
            
            else:
                #print(clientname,campaign_name)
                q1 = "select id from q_app_requirements where name='{}' and  campaign_name='{}'".format(clientname,campaign_name)
                cur.execute(q1)
                data = list(cur.fetchone())
                #print(data[0])
                user_report(
                    clientname=clientname,
                    campaign_name=campaign_name,
                    date=request.POST.get('date'),
                    no_of_impressions=request.POST.get('no_of_impressions'),
                    no_of_clicks=request.POST.get('no_of_clicks'),
                    cost_per_impressions=request.POST.get('cost_per_impressions'),
                    cost_per_click=request.POST.get('cost_per_click'),
                    total_cost_per_impressions=request.POST.get('total_cost_per_impressions'),
                    total_cost_per_click=request.POST.get('total_cost_per_click'),
                    cost_per_day=request.POST.get('cost_per_day'),
                    clientid_id= int(data[0])
                ).save()
                q1 = 'select DISTINCT deptid_id ,clientname from q_app_clientdetails inner join q_app_requirements on q_app_clientdetails.id =  deptid_id;'
                cur.execute(q1)
                people = list(cur.fetchall())
                conn.commit()
                empcontext = requirements.objects.all()    
                #people = clientdetails.objects.all()
                context={'people':people,'empcontext':empcontext}
                #messages.error(request,"Given Date Already Registered !")  
                #return render(request,'user_report.html',context)
                messages.success(request,'Form Submitted Successfully')
                return render(request,'user_report.html',context)

#--------------------------------------------------------------------------------------------------------------------



def report_user(request):
    cur,conn= sqlconn()
    if request.method=='GET':
        #people = clientdetails.objects.all()
        #deptcontext = clientdetails.objects.all()
        q1 = 'select DISTINCT deptid_id ,clientname from q_app_clientdetails inner join q_app_requirements on q_app_clientdetails.id =  deptid_id;'
        cur.execute(q1)
        people = list(cur.fetchall()) 
        empcontext = requirements.objects.all()    
        context={'people':people,'empcontext':empcontext}
        #print(people ,'\n', empcontext)
        return render(request,'user_report_user.html',context)
    
    elif request.method=='POST':
        clientname=request.POST.get('hiddenclient')
        campaign_name=request.POST.get('hiddencampaign')
        if clientname == '' and campaign_name == '':
            messages.error(request,'Select Client And Campaign Data')
            return render(request,'user_report.html',context)
        else:
            clientname = clientname.replace("\r\n"," ")
            clientname = clientname.strip()
            campaign_name=campaign_name.replace("\r\n"," ")
            #print(campaign_name)
            campaign_name=campaign_name.strip()
            date=request.POST['date']
        if user_report.objects.filter(Q(date=date) & Q (clientname=clientname) & Q(campaign_name=campaign_name)).exists(): # it checks client name is already registered or not
            q1 = 'select DISTINCT deptid_id ,clientname from q_app_clientdetails inner join q_app_requirements on q_app_clientdetails.id =  deptid_id;'
            cur.execute(q1)
            people = list(cur.fetchall()) 
            #people = clientdetails.objects.all()
            empcontext = requirements.objects.all()    
            context={'people':people,'empcontext':empcontext}
            messages.error(request,"Given Date Already Registered !")  
            return render(request,'user_report_user.html',context)
        
        else:
            clientname=request.POST.get('hiddenclient')
            clientname = clientname.replace("\r\n","")
            clientname = clientname.strip()
            campaign_name=request.POST.get('hiddencampaign')
            campaign_name=campaign_name.replace("\r\n","")
            #print(campaign_name)
            campaign_name=campaign_name.strip()
            #print(clientname,campaign_name)
            q1 = "select id from q_app_requirements where name='{}' and  campaign_name='{}'".format(clientname,campaign_name)
            cur.execute(q1)
            data = list(cur.fetchone())
            #print(data)
            #print(data[0])
            user_report(
                clientname=clientname,
                campaign_name=campaign_name,
                date=request.POST.get('date'),
                no_of_impressions=request.POST.get('no_of_impressions'),
                no_of_clicks=request.POST.get('no_of_clicks'),
                cost_per_impressions=request.POST.get('cost_per_impressions'),
                cost_per_click=request.POST.get('cost_per_click'),
                total_cost_per_impressions=request.POST.get('total_cost_per_impressions'),
                total_cost_per_click=request.POST.get('total_cost_per_click'),
                cost_per_day=request.POST.get('cost_per_day'),
                clientid_id= int(data[0])
            ).save()
            q1 = 'select DISTINCT deptid_id ,clientname from q_app_clientdetails inner join q_app_requirements on q_app_clientdetails.id =  deptid_id;'
            cur.execute(q1)
            people = list(cur.fetchall()) 
            conn.commit()
            empcontext = requirements.objects.all()    
            #people = clientdetails.objects.all()
            context={'people':people,'empcontext':empcontext}
            #messages.error(request,"Given Date Already Registered !")  
            #return render(request,'user_report.html',context)
            messages.success(request,'Form Submitted Successfully')
            return render(request,'user_report_user.html',context)

    

