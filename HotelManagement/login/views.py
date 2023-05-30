from django.shortcuts import render, HttpResponse
from .models import login
usern='none'  #any user login with any above cradential it will store into this obj

def loginpage(request):
    global usern

    
    #print(request)
    if request.method == 'GET':
        usern='none'
        return render(request,'loginpage.html')
    else: #login authentication
        username=request.POST.get('username') #storing fields data in variable
        password=request.POST.get('password')
        print(username,password)
        #print('a',username,password)
        uname=login.objects.filter(username=username)#validating fields data with databse
        pwd=login.objects.filter(password=password)
        #print('b:',uname,pwd)
        if uname and pwd: #if true only it will send who gonna login as user
            dsig = login.objects.filter(username=username)
            for i in dsig:
                dsg=i.designation 
                if dsg =='Manager':
                    usern='Manager'
                    return render(request,'user.html',{'d':'Manager'})
                elif dsg =='Admin':
                    usern='Admin'
                    return render(request,'user.html',{'d':'Admin'})
                elif dsg=='Receptionist':
                    usern='Receptionist'
                    return render(request,'user.html',{'d':'Receptionist'})
        else:#otherwise it sending none for (INVALID DETAILS)
             return render(request,'loginpage.html',{'d':'none'})

            

'''this function will call when user click on back button'''     
def user(request):
    if usern =='Manager':
        return render(request,'user.html',{'d':'Manager'})
    elif usern == 'Admin':
        return render(request,'user.html',{'d':'Admin'})
    elif usern=='Receptionist':
        return render(request,'user.html',{'d':'Receptionist'})
    else:
        #return render(request,'user.html',{'d':'none'})
        return HttpResponse('SESSION OVER! PLEASE LOGIN AGAIN')
    
def userdata():
    return usern
