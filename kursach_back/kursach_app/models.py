from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Company(models.Model):
    Name = models.CharField(max_length=30)
    Ticker = models.CharField(max_length=5)
    Picture = models.CharField(max_length=100, null=True)
    Number_of_shares = models.IntegerField()
    Country = models.CharField(max_length=30)
    Currency = models.CharField(max_length=30, default='dollar')

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return f"{self.Name} - {self.Ticker}"

class Stocks(models.Model):
    Time = models.DateTimeField(primary_key=True, auto_now_add=True)
    Price = models.FloatField()
    Company_id = models.ForeignKey('Company', on_delete=models.CASCADE)
    Change_percent = models.FloatField()

class User(AbstractUser):
    Status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"

class Portfolio(models.Model):
    User_id = models.ForeignKey('User', on_delete=models.CASCADE)
    Company_id = models.ForeignKey('Company', on_delete=models.CASCADE)
    Number_of_shares = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Portfolio'

    
class Operations(models.Model):
    User_id = models.ForeignKey('User', on_delete=models.CASCADE)
    Company_id = models.ForeignKey('Company', on_delete=models.CASCADE)
    Date_time = models.DateTimeField(auto_now_add=True)
    Number_of_shares = models.IntegerField(default=0)
    Price = models.FloatField()

    class Meta:
        verbose_name_plural = 'Operations'
