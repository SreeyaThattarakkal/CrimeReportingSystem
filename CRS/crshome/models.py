from distutils.command.upload import upload
import email
from hashlib import blake2b
from random import choices
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

userchoices = (
    (1,"ADMIN"),
    (2,"PUBLIC"),
    (3,"POLICE")
)
complaint_choices = (
    ("FILED","FILED"),
    ("ACCEPTED","ACCEPTED"),
    ("REJECTED","Rejected")
)
police_choices = (
    ("DGP","DGP"),
    ("SI","SI"),
    ("CI","CI"),
    ("SP","SP"),
    ("ASP","ASP"),
    ("ASI","ASI"),
    ("CONSTABLE","CONSTABLE")
)
fir_choices = (
    ("REGISTERED","Registered"),
    ("SOLVED","Solved")
)
class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number','username']

    name = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.IntegerField(default=1,choices=userchoices)
    # phone_code = models.CharField(max_length=4,null=True,blank=True)
    phone_number = models.CharField(max_length=13,null=True,blank=True)
    email = models.EmailField(null=True,blank=True,unique=True)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=155,null=True,blank=True)
    pincode = models.CharField(max_length=6,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    station = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=155,choices=police_choices,null=True,blank=True)
    image = models.ImageField(upload_to='user_images/dp/',null=True,blank=True)
    police_id = models.CharField(max_length=13,unique=True,null=True,blank=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username

class Complaint(models.Model):
    complaint_code = models.CharField(max_length=30,null=True,blank=True)
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=13,null=True,blank=True)
    title = models.CharField(max_length=255)
    details = models.TextField(null=True,blank=True)
    place = models.CharField(max_length=255)
    time = models.DateTimeField()
    pincode = models.CharField(max_length=10)
    status = models.CharField(max_length=25,choices=complaint_choices,default="FILED")
    photo = models.ImageField(null=True,blank=True,upload_to="crimeimages/")
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FIR(models.Model):
    fir_code = models.CharField(max_length=30,null=True,blank=True)
    complaint = models.ForeignKey(Complaint,on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=30,choices=fir_choices,default="REGISTERED")
    assignee = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    soft_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    extra_notes = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.complaint.title

class Feedback(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    case = models.ForeignKey(Complaint,on_delete=models.SET_NULL,null=True)
    text = models.TextField(blank=True)
    rating = models.FloatField(default=5.0)
    soft_delete = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user} {self.rating}'


class Blocked(models.Model):
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return self.phone_number


class Notification(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.text