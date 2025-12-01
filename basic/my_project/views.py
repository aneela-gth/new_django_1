from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import json
from .models import Student
from .models import post
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from my_project.models import Users
import jwt
from django.conf import settings
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo


# Create your views here.
def sample(request):
    return HttpResponse('hello world')
def sample1(request):
    return HttpResponse('welocome to dijango')
def sampleinfo(request):
    # data={"name":"aneela","age":23}
    data={"result":[4,6,8,9]}
    return JsonResponse(data)

def dynamicresponse(request):
    name=request.GET.get("name","krishna")
    city=request.GET.get("city","hyd")
    return HttpResponse(f"hello {name} from {city}")
def sum(request):
    a=2
    b=3
    sum=a+b
    return HttpResponse(sum)
def sub(request):
    x=20
    y=10
    sub=x-y
    return HttpResponse(sub)
def mult(request):
    c=20
    d=5
    mult=c*d
    return HttpResponse(mult)
def sum1(request):
    a= request.GET.get('a',10)
    b=request.GET.get('b',20)
    result = a + b
    return HttpResponse(f"The sum1 is: {result}")
def mult1(request):
    x=request.GET.get('x',10)
    y=request.GET.get('y',20)
    result=x*y
    return HttpResponse(f"the mult1 is:{result}")
def sub1(request):
    c=request.GET.get('c',80)
    d=request.GET.get('d',20)
    result1=c-d
    return HttpResponse(f"the sub1 is:{result1}")
def health(request):
    try:
        with connection.cursor() as c:
            c.execute("SELECT1")
        return JsonResponse({"status":"ok","db":"connection"})
    except Exception as e:
        return JsonResponse({'status':"error","db":str(e)})


@csrf_exempt
def addStudent(request):  
    print(request.method)
    if request.method=='POST':
        data=json.loads(request.body)
        student=Student.objects.create(
            name=data.get('name'),
            age=data.get('age'),
            email=data.get('email')
            )
        
        return JsonResponse({"status":"success","id":student.id},status=200)
    
    elif request.method=="GET":
        result=list(Student.objects.values())
        print(result)
        return JsonResponse({"status":"success","data":result},status=200)


# get all records
        # results=list(Student.objects.all().values())
        # return JsonResponse({"status":"ok","data":results},status=200)

# get a specific record by id
    # data=json.loads(request.body)
    # ref_id=data.get("id")
    # results=list(Student.objects.filter(id=ref_id).values())
    # return JsonResponse({"status":"ok","data":results},status=200)


 # # filter by age>=20
    #     data=json.loads(request.body)
    #     ref_age=data.get("age")
    #     results=list(Student.objects.filter(age__gte=ref_age).values())
    #     return JsonResponse({"status":"ok","data":results},status=200)

    # # filter by age<=25
    #    data=json.loads(request.body)
    #    ref_age=data.get("age")
    #    results=list(Student.objects.filter(age__lte=ref_age).values())
    #    return JsonResponse({"status":"ok","data":results},status=200)
     
    # #  order by name
    #     result=list(Student.objects.order_by('name').values())
    #     return JsonResponse({"status":"ok","data": result},status=200)
      
    
     # get unique ages
        # results=list(Student.objects.values('age').distinct())
        # return JsonResponse({"status":"ok","data":results},status=200)
    
    # count total students
        # results=Student.objects.count()
        # return JsonResponse({"status":"ok","data":results},status=200)
    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id")
        new_email=data.get("email")
        existing_student=Student.objects.get(id=ref_id)
        # print(existing_student)
        existing_student.email=new_email
        existing_student.save()
        updated_data=Student.objects.filter(id=ref_id).values().first()
        return JsonResponse({"status":"data updated successfully","updated_data":updated_data},status=200)
    
    elif request.method=="DELETE":
         data=json.loads(request.body)
         ref_id=data.get("id")
         get_deleted_data=list(Student.objects.filter(id=ref_id).values())
         to_be_deleted=delete_data=Student.objects.get(id=ref_id)
         to_be_deleted.delete()
         return JsonResponse({"status":"succes","message":"student details deleted successfully","deleted_data":get_deleted_data},status=200)
    return JsonResponse({"error":"use post method"},status=400)


@csrf_exempt
def addpost(request):
    print(request.method)
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            new_post=post.objects.create(
                post_name=data.get('post_name'),
                post_type=data.get('post_type'),
                post_date=data.get('post_date'),
                post_description=data.get('post_description')
            )
            return JsonResponse({
                "status":"succes",
                "id":new_post.id,
                "message":"post created successfully"
            },status=201)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=400)
    return JsonResponse({"error":"use post method"},status=400)


def job1(request):
    return JsonResponse({"message":"u have successfully applied for job1"},status=200)
def job2(request):
    return JsonResponse({"message":"u have successfully applied for job2"},status=200)


@csrf_exempt
def signUp(request):
    if request.method=='POST':
        data = json.loads(request.body)
        print(data)
        user=Users.objects.create(
            username=data.get('username'),
            email=data.get('email'),
            password=make_password(data.get('password'))
            
            )
    return JsonResponse({"status":"success"},status=200)


# @csrf_exempt
# def login(request):
#     if request.method == "POST":
#         data = request.POST
#         print(data)

#         username = data.get("username")
#         password = data.get("password")

#         if not username or not password:
#             return JsonResponse(
#                 {"status": "failure", "message": "username and password required"},
#                 status=400
#             )
#         user = Users.objects.filter(username=username).first()
#         if user is None:
#             return JsonResponse(
#                 {"status": "failure", "message": "user not found"},
#                 status=400
#             )
#         if check_password(password, user.password):
#             # token="a json web token"
#             payload={"username":username,"email":user.email,"id":user.id}

#             token=jwt.encode(payload,settings.SECRET_KEY,algorithm='Hs256')
#             return JsonResponse(
#                 {"status": "success", "message": "successfully logged in",'token':token},
#                 status=200
#             )
#         else:
#             return JsonResponse(
#                 {"status": "failure", "message": "invalid password"},status=400)

# ---------------------------------------------------------------------

# @csrf_exempt
# def login(request):
#     if request.method == "POST":
#         data = request.POST
#         print(data)

#         username = data.get("username")
#         password = data.get("password")

#         if not username or not password:
#             return JsonResponse(
#                 {"status": "failure", "message": "username and password required"},
#                 status=400
#             )

#         user = Users.objects.filter(username=username).first()
#         issused_time=datetime.now(zoneinfo("Asia/kolkatha"))
#         if user is None:
#             return JsonResponse(
#                 {"status": "failure", "message": "user not found"},
#                 status=400
#             )

#         if check_password(password, user.password):

#             payload = {
#                 "username": username,
#                 "email": user.email,
#                 "id": user.id
#             }
#             payload={"username":username,"email":user.email,"id":user.id,"issused_time":issused_time}
#             token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


#             return JsonResponse(
#                 {"status": "success", "message": "successfully logged in", "token": token,"issued_at":issused_time},
#                 status=200
#             )

#         return JsonResponse({"status": "failure", "message": "invalid password"}, status=400)
# ---------------------------------------------------------------------------


@csrf_exempt
def login(request):
    if request.method=="POST":
        data=request.POST
        print(data)
        username=data.get('username')
        password=data.get("password")        
        try:
            user=Users.objects.get(username=username)
            issued_time=datetime.now(ZoneInfo("Asia/Kolkata"))
            expired_time=issued_time+timedelta(minutes=25)
            if check_password(password,user.password):
                # token="a json web token"
                #creating jwt token
                payload={"username":username,"email":user.email,"id":user.id,"exp":expired_time}
                token=jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
                return JsonResponse({"status":'successfully loggedin','token':token,"issued_at":issued_time,"expired at":expired_time,"expired_in":int((expired_time-issued_time).total_seconds()/60)},status=200)
            else:
                return JsonResponse({"status":'failure','message':'invalid password'},status=400)
        except Users.DoesNotExist:
            return JsonResponse({"status":'failure','message':'user not found'},status=400)












@csrf_exempt
def check(request):
    hashed="pbkdf2_sha256$600000$mi5aiszP0Yzo6tyPIHbQzs$MWaeuM4rrxJ3XyAPmM/33SZKRcJIBKtrlh4kF6nle/c="
    ipdata=request.POST
    print(ipdata)
    # hashed=make_password(ipdata.get("ip"))
    x=check_password(ipdata.get("ip"),hashed)
    return JsonResponse({"status":"success","data":x},status=200)

