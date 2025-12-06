"""
URL configuration for basic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from my_project.views import sample,sample1,sampleinfo,dynamicresponse,sum,sub,mult,sum1,mult1,sub1,health
from my_project.views import addStudent,addpost,job1,job2,signUp,check,login,getAllusers,home,aboutus,welcome,contact,services,projects
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sample/' ,sample),
    path('sample1/',sample1),
    path('sampleinfo/',sampleinfo),
    path('dynamicresponse/',dynamicresponse),
    path('sum/',sum),
    path('sub/',sub),
    path('mult/',mult),
    path('sum1/',sum1),
    path('mult1/',mult1),
    path("sub1/",sub1),
    path('health/',health),
    path('add/',addStudent),
    path('addpost/',addpost),
    path("job1/",job1),
    path('job2/',job2),
    path('signup/',signUp),
    path('check/',check),
    path('login/',login),
    path('users/',getAllusers),
    path('home/',home ,name='home'),
    path('about/', aboutus, name='about'),
    path('welcome/', welcome, name='welcome'),
    path('contact/', contact, name='contact'),
    path('services/', services, name='services'),
    path('projects/', projects, name='projects'),



]
