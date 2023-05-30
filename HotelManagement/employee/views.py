from django.shortcuts import render,HttpResponse
from employee.models import employeedetails
from login.views import userdata


'''this function used to insert employee forms field to db by using django ORM'''
def employeeform(request):
    user=userdata()
    print(user)
    if request.method=='GET':
        if user=='none':
            return HttpResponse('SESSION OVER! PLEASE LOGIN AGAIN')
        return render(request,'employeeform.html',{'d':user})
    else:
      
       employeedetails(
            EMPLOYEE_NAME=request.POST.get('EMPLOYEE_NAME'),
            DATE_OF_JOINING=request.POST.get('DATE_OF_JOINING'),
            SALARY=request.POST.get('SALARY'),
            MOBILE=request.POST.get('MOBILENUMBER'),
            DESIGNATION=request.POST.get('DESIGNATION'),
            GENDER=request.POST.get('GENDER')
        ).save()
       return render(request,'employeeform.html',{'d':user})
    
'''this function used to display emp deatils'''
def empdetails(request):
    user=userdata()
    print(user)
    if user=='none':
        return HttpResponse('SESSION OVER! PLEASE LOGIN AGAIN')
    empdat=employeedetails.objects.all().values()
    return render(request,'empdetails.html',{'empdat':empdat,'d':user})