from django.shortcuts import render , redirect ,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import *
from django.db.models import Sum
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .tasks import send_email_background
# Create your views here.
def index(request):
 return render(request , "index.html")

def application_form(request):
  if request.method=='POST':
   fullName=request.POST['fullName']
   maritalStatus=request.POST['maritalStatus']
   email=request.POST['Email']
   address=request.POST['address']
   contact=request.POST['contact']
   CNIC_text=request.POST['CNIC']
   cnicUpload=request.FILES.get('cnicUpload')
   employmentStatus=request.POST['employmentStatus']
   organization=request.POST['organization']
   income=request.POST['income']
   loanAmount=request.POST['loanAmount']
   intrest=request.POST['intrest']
   loanPurpose=request.POST['loanPurpose']
   loanTerm=request.POST['loanTerm']
   
   details=Loan.objects.create(
     user=request.user,
     Email = email ,
     fullname=fullName,
     address=address,
     contact=contact,
     martrial_status=maritalStatus,
     CNIC=CNIC_text,
     employment_status=employmentStatus,
     monthly_income=income,
     image=cnicUpload,
     organization_name=organization,
     Ammount=loanAmount,
     intrest=intrest,
     purpose=loanPurpose,
     duration=loanTerm,
     
     )
   
   details.save()
   
   subject="New application recived"
   message=f"{fullName} has applied for loan go to the dashboard and review the application!"
   to_list=[email]
   
   send_email_background(subject,message,to_list)
   
   return redirect('dashboard') 
  return render(request,"application_form.html")

def login_user(request):
 if request.method == 'POST':
  username=request.POST['username']
  password=request.POST['password']
  
  user=authenticate(username=username,password=password)
  if user is not None:
    print(user)
    if not user.is_staff:
      auth_login(request,user)
      return redirect('dashboard')
    else:
      auth_login(request,user)
      return redirect('admin-dashboard')
  
  return render(request, 'login.html')
 return render(request, 'login.html')
 
def logout_user(request):
 
 auth_logout(request)
 return redirect('index')

def register(request):
 if request.method == 'POST':
  uname=request.POST['username']
  firstname=request.POST['firstName']
  lastname=request.POST['lastName']
  mail=request.POST['email']
  passw=request.POST['password']
  confirm_password=request.POST['confirmPassword']
  
  myuser=User.objects.create_user(username=uname, email=mail, password=passw)
  myuser.first_name=firstname
  myuser.last_name=lastname
  myuser.save()
  print("user craeted")
  
  return redirect('login_user')
 
 return render(request , 'registration.html')

def dashboard(request):
 return render(request,'dashboard.html')  

def Application(request):
 try:
  application = Loan.objects.filter(user__username=request.user,status="pending")
 except Loan.DoesNotExist:
  application = None
 return render(request,'applications.html', {'applications':application})

def update_profile(request):
  if request.method=="POST":
   username=request.POST['username'] 
   firtname=request.POST['firstname'] 
   lastname=request.POST['lastname'] 
   email=request.POST['email'] 
   
   myuser=User.objects.get(id=request.user.id)
   myuser.username=username
   myuser.first_name=firtname
   myuser.last_name=lastname
   myuser.email=email
   myuser.save()
   
   messages.success(request,"Data Updated successfully")
   return redirect("update_profile")
   
  return render(request,'update_profile.html', {'user':request.user})

def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login_user') 

    total_amount = Loan.objects.filter(status="approved").aggregate(Sum('intrest'))
    active_loans=len(Loan.objects.filter(status="approved"))
    total_borrowers=len(Loan.objects.filter(status="pending"))
    
    return render(request, 'admin/admin.html',{'total_amount':total_amount, 'active_loans':active_loans, 'total_borrowers':total_borrowers})

def view_users(request):
  users=User.objects.all().exclude(is_staff=True)
  return render(request,"admin/users.html",{"users":users})

def update_application(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        maritalStatus = request.POST['maritalStatus']
        address = request.POST['address']
        contact = request.POST['contact']
        email = request.POST['email']
        CNIC_text = request.POST['CNIC']
        cnicUpload = request.FILES.get('cnicUpload')
        employmentStatus = request.POST['employmentStatus']
        monthlyIncome = request.POST['monthlyIncome']
        organizationName = request.POST['organizationName']
        loanAmount = request.POST['loanAmount']
        interest = request.POST['intrest']
        loanTerm = request.POST['loanTerm']
        loanPurpose = request.POST['loanPurpose']
        app_id=request.POST['applicationID']

        try:
            loan = Loan.objects.get(id=app_id)
            loan.Email = email
            loan.fullname = fullname
            loan.address = address
            loan.contact = contact
            loan.martrial_status = maritalStatus
            loan.CNIC = CNIC_text
            loan.employment_status = employmentStatus
            loan.monthly_income = monthlyIncome
            loan.image = cnicUpload
            loan.organization_name = organizationName
            loan.Ammount = loanAmount
            loan.intrest = interest
            loan.purpose = loanPurpose
            loan.duration = loanTerm
            loan.save()

            messages.success(request, "Data updated successfully")
            return redirect('Application')

        except Loan.DoesNotExist:
            messages.error(request, "Application not found")
            return redirect('Application')

    messages.error(request, "An error occurred while updating. Please try again later.")
    return redirect('Application')

def admin_applictaions(request):
  applications= Loan.objects.filter(status="pending")
  return render(request,'admin/applications.html' ,{'applications':applications})

def Approvals(request,id):
  uid=id
  application=Loan.objects.get(id=uid)
  application.status="approved"
  application.loan_holder=True
  application.save()
  
  subject=f"Congrats {application.fullname}"
  message=" Congrats! your application has been approved by the admin please visit out Nearest office for futher details and avail loan"
  to_list=[application.Email]
  
  send_email_background(subject, message, to_list)
  
  return redirect('admin-applications')
  
def Rejections(request,id):
  uid=id
  application=Loan.objects.get(id=uid)
  application.status="rejected"
  application.save()
  
  subject=f"Sad {application.fullname}"
  message=" sorry! your application has been rejected by the admin please visit out Nearest office for futher details and avail loan"
  to_list=[application.Email]
  
  send_email_background(subject,message,to_list)
  return redirect('admin-applications')

def approved(request):
  applications=Loan.objects.filter(status="approved")
  return render(request, 'admin/approved.html', {'applications':applications})

def rejestion(request):
  applications=Loan.objects.filter(status="rejected")
  return render(request, 'admin/rejestion.html', {'applications':applications})

def loan_products(request):
  return render(request,'loan_products.html')

def loan_calculator(request):
  return render(request, 'loan_calculator.html')

def talk_to_expert(request):
  return render(request, 'talk_to_expert.html')

def aboutus(request):
  return render(request, 'aboutus.html')

def contactus(request):
  return render(request, 'contactus.html')