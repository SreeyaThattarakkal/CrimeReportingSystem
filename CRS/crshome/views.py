from multiprocessing import context
import re
from django import http
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from crshome.models import FIR, Blocked, Complaint, Feedback, Notification, User
from django.contrib import messages
from datetime import date
from django.http import JsonResponse
# Create your views here.


def loginFunction(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(email=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:dashboard')
        else:
            messages.add_message(request, messages.WARNING,
                                 'Please verify credentials you entered!'
                                 )
            return redirect('home:login')
    return render(request,'login.html')

def logoutView(request):
    logout(request)
    return redirect('home:login')


def Reg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        password = request.POST.get('password')
        user = User.objects.create(name=name,user_type=2,email=email,phone_number=phone,city=city,pincode=pincode,address=address,username=email)
        user.set_password(password)
        user.save()    
        return redirect('home:login')
    return render(request,'register.html')

@login_required
def Police_reg(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # city = request.POST.get('city')
        # pincode = request.POST.get('pincode')
        # address = request.POST.get('address')
        password = request.POST.get('password')
        station = request.POST.get('station')
        designation = request.POST.get('designation')
        police_id = request.POST.get('police-id')
        user = User.objects.create(user_type=3,name=name,email=email,username=email,phone_number=phone,station=station,designation=designation,police_id=police_id)
        user.set_password(password)
        user.username = email
        user.save()
        return redirect('home:policelist')
    context = {
        'user_type':user.user_type,
    }  
    if request.user.user_type == 1 or request.user.user_type == 3:
        return render(request,'police_reg.html',context)    
    else:
        return HttpResponse("Page Not Found") 

@login_required
def Police_list(request):
    if request.user.user_type == 1 or request.user.user_type == 3:
        police = User.objects.filter(user_type=3)
        count = 0
        if  request.user.user_type == 3:
            count = Notification.objects.filter(user=request.user,read=False).count()
        return render(request,'police_list.html',{'police':police,'user_type':request.user.user_type,'count':count}) 
    else:
        return HttpResponse("Page Not Found")       

@login_required
def Dashboard(request):
    user = request.user
    newly_users = User.objects.filter(user_type=2)[:5]
    today = date.today()
    num = today.month 
    year = today.year 
    if num - 1 == 0:
        num = 13
    num -= 1
    year -= 1
    array = ['0','1','2','3','4','5']
    li = []
    for i in array:
        li.append((num,year))
        if num - 1 == 0:
            num = 13
            year -= 1
        num -= 1
    new_lst = li[::-1]
    crime_count = []
    count = 0
    if user.user_type == 2 or user.user_type == 3:
        count = Notification.objects.filter(user=user,read=False).count()
    for n in new_lst:
        crime = Complaint.objects.filter(time__year=n[1],time__month=n[0],soft_delete=False).count()
        crime_count.append(crime)
    context = {
        'new_users':newly_users,
        'crime_count':crime_count,
        'user_type':user.user_type,
        'count':count
    }
    return render(request,'dashboard.html',context)

@login_required
def Userlist(request):
    if request.user.user_type == 1 or request.user.user_type == 3:
        users = User.objects.filter(user_type=2)
        context = {
             'user_type': request.user.user_type,
            'users':users
        }
        return render(request,'userlist.html',context)
    else:
        return HttpResponse("Page Not Found")

@login_required
def ComplaintsList(request):
    complaints = Complaint.objects.filter(soft_delete=False)
    user = request.user
    count = 0
    if user.user_type == 2 or user.user_type == 3:
        count = Notification.objects.filter(user=user,read=False).count()
    return render(request,'complaints.html',{'complaints':complaints,'user_type':user.user_type,'count':count})

@login_required
def FirList(request):
    if request.user.user_type == 1:
        fir = FIR.objects.filter(soft_delete=False)
        return render(request,'fir.html',{'fir':fir,'user_type':request.user.user_type})
    elif request.user.user_type == 3:
        count = Notification.objects.filter(user=request.user,read=False).count()
        fir = FIR.objects.filter(soft_delete=False,assignee=request.user)
        return render(request,'fir.html',{'fir':fir,'user_type':request.user.user_type,'count':count})
    else:
        return HttpResponse("Page Not Found")

@login_required
def FeedbackList(request):
    if request.user.user_type == 1:
        feedbacks = Feedback.objects.filter(soft_delete=False)
        return render(request,'feedbacks.html',{'feedbacks':feedbacks,'user_type':request.user.user_type})
    elif request.user.user_type == 2:
        count = Notification.objects.filter(user=request.user,read=False).count()
        feedbacks = Feedback.objects.filter(soft_delete=False,user=request.user)
        return render(request,'feedbacks.html',{'feedbacks':feedbacks,'user_type':request.user.user_type,'count':count})
    else:
        return HttpResponse("Page Not Found")

@login_required
def DeleteFeedback(request,id):
    if request.user.user_type == 1:
        feedback = Feedback.objects.get(id=id)
        feedback.soft_delete = True
        feedback.save()
        return redirect('home:feedbacks')
    else:
        return HttpResponse("Page Not Found")

@login_required
def DeleteFir(request,id):
    if request.user.user_type == 1:
        fir = FIR.objects.get(id=id)
        fir.soft_delete = True
        fir.save()
        return redirect('home:fir')
    else:
        return HttpResponse("Page Not Found")

@login_required
def DeletePolice(request,id):
    if request.user.user_type == 1:
        police = User.objects.get(id=id)
        police.delete()
        return redirect('home:policelist')
    else:
        return HttpResponse("Page Not Found")

@login_required
def BlockUser(request,id):
    if request.user.user_type == 1:
        user = User.objects.get(id=id)
        if user.is_active == True:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('home:userlist')
    else:
        return HttpResponse("Page Not Found")

@login_required
def Firreg(request,id):
    user = request.user
    complaint=Complaint.objects.get(id=id)
    police = User.objects.filter(user_type=3)
    return render(request,'fir_register.html',{'complaint':complaint,'police':police,'user_type': user.user_type})

@login_required
def Addfir(request):
        fir_code = request.POST.get('fir_code')
        complaint = request.POST.get('complaint')
        complaint_id = Complaint.objects.get(complaint_code=complaint) 
        police = request.POST.get('police')
        police_id = User.objects.get(id=police) 
        extra = request.POST.get('extra')
        FIR.objects.create(fir_code=fir_code,complaint=complaint_id,status="REGISTERED",assignee=police_id,extra_notes=extra)  
        text = "Your Complaint '{comp}' of code {code} has been accepted and assigned to {des} - {police} ".format(code=complaint_id.complaint_code,comp=complaint_id.title,des=police_id.designation,police=police_id.name)
        text2 = "New Fir assigned to you! case details - '{comp}' of code {code} ".format(code=complaint_id.complaint_code,comp=complaint_id.title)
        if complaint_id.user:
            Notification.objects.create(user=complaint_id.user,read=False,text=text) 
        Notification.objects.create(user=police_id,read=False,text=text2) 
        complaint_id.status="ACCEPTED"
        complaint_id.save() 
        return redirect('home:fir')

@login_required
def Firreject(request,id):
    complaint = Complaint.objects.get(id=id)
    if complaint.user:
        text = "Your Complaint '{comp}' of code {code} has been rejected! ".format(code=complaint.complaint_code,comp=complaint.title)
        Notification.objects.create(user=complaint.user,read=False,text=text)
    complaint.status="REJECTED"
    complaint.save()
    return redirect('home:complaints')


@login_required
def FileComplaint(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('title') 
        details = request.POST.get('details') 
        place = request.POST.get('place') 
        pincode = request.POST.get('pincode') 
        time = request.POST.get('time') 
        photo = request.FILES.get('photo') 
        complaint = Complaint.objects.create(user=request.user,title=title,details=details,place=place,pincode=pincode,
                time=time,photo=photo)
        complaint.complaint_code = 'COMP{}'.format(complaint.id)
        complaint.save()
        return redirect('home:complaints')
    if user.user_type == 2:
        count = Notification.objects.filter(user=request.user,read=False).count()
        return render(request,'file-complaint.html',{'user_type':user.user_type,'count':count})
    else:
        return HttpResponse("Page not found")

@login_required
def CreateFeedback(request):
    user = request.user
    if request.method == 'POST':
        case = request.POST.get('case') 
        text = request.POST.get('text') 
        rating = request.POST.get('rating') 
        case_new = Complaint.objects.get(id=case)
        feedback = Feedback.objects.create(user=request.user,case=case_new,text=text,rating=rating)
        return redirect('home:feedbacks')
    if user.user_type == 2:
        count = Notification.objects.filter(user=user,read=False).count()
        case = Complaint.objects.filter(user=request.user)
        return render(request,'create-feedback.html',{'user_type':user.user_type,'cases':case,'count':count})
    else:
        return HttpResponse("Page not found")


def NoneuserFileComplaint(request):
    if request.method == 'POST':
        title = request.POST.get('title') 
        details = request.POST.get('details') 
        name = request.POST.get('name') 
        phone = request.POST.get('phone') 
        place = request.POST.get('place') 
        pincode = request.POST.get('pincode') 
        time = request.POST.get('time') 
        photo = request.FILES.get('photo') 
        complaint = Complaint.objects.create(title=title,details=details,place=place,pincode=pincode,time=time,photo=photo,phone_number=phone,name=name)
        complaint.complaint_code = 'COMP{}'.format(complaint.id)
        complaint.save()
        return redirect('home:login')
    return render(request,'nonereg_complaint.html')

@login_required
def blockNumber(request,num):
    if request.user.user_type == 1:
        Blocked.objects.create(phone_number=num)
        return redirect('home:complaints')
    return HttpResponse("Page not found")

@login_required
def MarkasRead(request,id):
    if request.user.user_type == 2 or request.user.user_type == 3:
        a = Notification.objects.get(id=id)
        a.read = True
        a.save()
        return redirect('home:notifications')
    return HttpResponse("Page not found")

@login_required
def BlockedList(request):
    if request.user.user_type == 1:
        blocked = Blocked.objects.all()
        return render(request,'blocked.html',{'blocked':blocked,'user_type':request.user.user_type})
    return HttpResponse("Page not found")

    
@login_required
def UnblockNum(request,id):
    if request.user.user_type == 1:
        blocked = Blocked.objects.get(id=id)
        blocked.delete()
        return redirect('home:blocked')
    else:
        return HttpResponse("Page Not Found")

def CheckBlocked(request):
    phone = request.GET.get('phone')
    try:
        ph = Blocked.objects.get(phone_number=phone)
    except:
        return JsonResponse({'exists': False})
    return JsonResponse({'exists': True})

def CheckEmail(request):
    email = request.GET.get('email')
    if request.user:
        if email == request.user.email:
            email = ''
    try:
        user = User.objects.get(email=email)
    except:
        return JsonResponse({'exists': False})
    return JsonResponse({'exists': True})

def CheckPoliceid(request):
    policeid = request.GET.get('policeid')
    try:
        user = User.objects.get(police_id=policeid)
    except:
        return JsonResponse({'exists': False})
    return JsonResponse({'exists': True})


@login_required
def Notifications(request):
    if request.user.user_type == 2 or request.user.user_type == 3:
        count = Notification.objects.filter(user=request.user,read=False).count()
        notifications = Notification.objects.filter(user=request.user).order_by('-id')
        return render(request,'notifications.html',{'notifications':notifications,'user_type':request.user.user_type,'count':count})
    else:
        return HttpResponse("Page Not Found")

@login_required
def Solvedfir(request,id):
    fir = FIR.objects.get(id=id)
    fir.status='SOLVED'    
    fir.save()   
    complaint_id = fir.complaint.user
    text = "Your Case of code '{code}' has been solved by {des} - {police}".format(code=fir.complaint.complaint_code,des=fir.assignee.designation,police=fir.assignee.name)
    Notification.objects.create(user=complaint_id,read=False,text=text) 
    return redirect('home:fir') 

@login_required
def ProfileEdit(request):
    user = request.user
    if request.user.user_type == 2:
        if request.method == 'POST':
            name = request.POST.get('name') 
            phone = request.POST.get('phone') 
            email = request.POST.get('email') 
            address = request.POST.get('address') 
            city = request.POST.get('city') 
            pincode = request.FILES.get('pincode') 
            user = request.user
            user.name ,user.phone_number , user.email , user.address = name , phone , email , address
            user.city , user.pincode  = city , pincode
            user.save()
            return redirect('home:dashboard')
        count = Notification.objects.filter(user=request.user,read=False).count()
        return render(request,'profile-edit.html',{'user_type':user.user_type,'user':user,'count':count})
    else:
        return HttpResponse("Page Not Found")