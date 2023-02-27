from django.db import models

# Create your models here.

class Company(models.Model):
    Name = models.CharField(max_length=30)
    Ticker = models.CharField(max_length=5)
    Picture = models.CharField(max_length=100, null=True)
    Number_of_shares = models.IntegerField()
    Country = models.CharField(max_length=30)
    Currency = models.CharField(max_length=30, default='dollar')

class Stocks(models.Model):
    Time = models.DateTimeField(primary_key=True, auto_now_add=True)
    Price = models.FloatField()
    Company_id = models.ForeignKey('Company', on_delete=models.CASCADE)
    Change_percent = models.FloatField()

class User(models.Model):
    Login = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    First_name = models.CharField(max_length=50)
    Email = models.EmailField()
    Administrator = models.BooleanField(default=False)
    Manager = models.BooleanField(default=False) 

class Portfolio(models.Model):
    User_id = models.ForeignKey('User', on_delete=models.CASCADE)
    Company_id = models.ForeignKey('Company', on_delete=models.CASCADE)
    Number_of_shares = models.IntegerField()
