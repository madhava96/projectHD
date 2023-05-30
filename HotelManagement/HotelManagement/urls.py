"""HotelManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from availibilty.views import show#,cancle
from booking.views import book,check
from login.views import loginpage,user
from employee.views import employeeform,empdetails

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',loginpage,name='login'),
    path('user',user,name='user'),
    path('show',show,name='show'),
    path('book',book, name='book'),
    path('check',check, name='check'),
    path('emp_form',employeeform,name='employeeform'),
    path('emp_details',empdetails,name='empdetails')
]
