from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Loan(models.Model):
    """status"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
        
    """USER DETAILS"""
    user=models.ForeignKey(User,on_delete=models.CASCADE, default=2)
    fullname=models.CharField(max_length=50, default='undefined')
    address=models.CharField(max_length=250,default='undefined')
    contact=models.IntegerField(default='0000')
    martrial_status = models.CharField(max_length=50, default='Single')
    CNIC = models.IntegerField(default=0)
    Email=models.EmailField(default='example@domin.com')

    """EMPLOYMENT DETAILS"""
    employment_status = models.CharField(max_length=100, default='Unemployed')
    monthly_income = models.IntegerField(default=0)
    image = models.ImageField(upload_to='Cnic/', default='default.jpg')  # Ensure 'default.jpg' exists in 'media/Cnic/'
    organization_name = models.CharField(max_length=100, default='N/A')

    """LOAN DETAILS"""
    Ammount = models.IntegerField(default=0)
    intrest = models.IntegerField(default=0)
    purpose = models.CharField(max_length=250, default='General')
    duration = models.CharField(max_length=50, default='6 Months')
    
    """Loan holder"""
    loan_holder=models.BooleanField(default=False)
    
    def __str__(self):
        return self.fullname
 