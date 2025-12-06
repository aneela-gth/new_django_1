
from django.http import JsonResponse
from my_project.models import Users
import re
import json
import jwt
from django.conf import settings

class indexMiddleware:
    def __init__(self,get_response):
          self.get_response=get_response
    def __call__(self,request):
         print(request,"hello")
         if(request.path=="/student/"):
           print(request.method,"method")
           print(request.path)
         elif(request.path=="/sum"):
            print(request.method,"method")
            print(request.path)
         elif(request.path=="/sample1"):
             print(request.method,"method")
             print(request.path)
         elif(request.path=="/sampleinfo"):
             print(request.method,"method")
             print(request.path)
             
         response=self.get_response(request)
         return response
class SscMiddleware:
    def __init__(self,get_response):
          self.get_response=get_response
    def __call__(self,request):
        if(request.path in["job1/","job2/"]):
            ssc_result=(request.GET.get("ssc"))
            print(ssc_result)
            if(not ssc_result):
                return JsonResponse({"error":"u should qulify atleats ssc for applying this job"},status=400)
        return self.get_response(request)

class MedicalFitMiddleware:
    def __init__(self,get_response):
          self.get_response=get_response
    def __call__(self,request):
        if(request.path=="job1/"):
            meddical_fit_result=(request.GET.get("midically_fit"))
            if(meddical_fit_result!='True'):
                return JsonResponse({"error":"u  not medically fit to apply for this job rule "},status=400)
        return self.get_response(request) 
class AgeMiddleware:
    def __init__(self,get_response):
          self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["job1/","job2/"]):
            Age_checker=int(request.GET.get("age",17))
            if((Age_checker>25 and Age_checker<18)):
                return JsonResponse({"error":"age must be in b/w 18 and 25"},status=400)
        return self.get_response(request) 
    

    
class UsernameMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path == "/signup/"):
            data=json.loads(request.body)
            username=data.get("username","")
            #checks username is empty or not
            if not username:
                return JsonResponse({"error":"username is required"},status=400)
            #checks length    
            if len(username)<3 or len(username)>20:
                return JsonResponse({"error":"username should contains 3 to 20 characters"},status=400)
            #checks starting and ending
            if username[0] in "._" or username[-1] in "._":
                return JsonResponse({"error":"username should not starts or ends with . or _"},status=400) 
            #checks allowed characters
            if not re.match(r"^[a-zA-Z0-9._]+$",username):
                return JsonResponse({"error":"username  should contains letters,numbers,dot,underscore"},status=400)
            #checks .. and  __
            if ".." in username or "__" in username:
                return JsonResponse({"error:cannot have .. or __"},status=400)   
        return self.get_response(request)        

class signupMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        data=json.loads(request.body)
        username=data.get("username")
        eamil=data.get("username")
        dob=data.get("dob")
        password=data.get("pswd")
        


            
class emailMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path == "/signup/"):
            data=json.loads(request.body)
            email=data.get("email","")
        #checks email is empty or not
            if not email:
                return JsonResponse({"error":"email is required"},status=400)
            # Basic email pattern
            
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$',email):
              return JsonResponse({"error": "Invalid email format"}, status=400)
            if Users.objects.filter(email=email).exists():
                return JsonResponse({"error":"Email already exists"},status=400)
        return self.get_response(request)  
    

class PasswordMiddleware:
    def __init__(self,get_response):  
        self.get_response=get_response
    def __call__(self,request): 
        if(request.path=="/signup/") :
            data=json.loads(request.body)
            Password=data.get("password")
            if not Password:
                return JsonResponse({"error":"password should not empty"},status=400)
            if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s]).{8,}$',Password):
                return JsonResponse({"error":"Password must contain at least 8 characters including uppercase, lowercase, number and special character"}, status=400)
            
        return self.get_response(request)
    

class AuthenticateMiddleware():
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if request.path=="/users/":
            token=request.headers.get("Authorization")
            print(token,"token")
            if not token:
                return JsonResponse({"error":"Authorization token missing"},status=401)
            token_value=token.split(" ")[1]
            print(token_value,"token_value")
            try:
                decoded_data=jwt.decode(token_value,settings.SECRET_KEY,algorithms=["HS256"])
                print(decoded_data,"decoded_data")
                print(request)
                request.token_data=decoded_data
                print(request.token_data,"after")
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error":"token has expired, please login again"},status=401)
            except jwt.exceptions.InvalidSignatureError:
                return JsonResponse({"error":"invalid token signature"},status=400)

        return self.get_response(request)



