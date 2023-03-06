from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=30, unique=True)
    ticker = models.CharField(max_length=5, unique=True)
    picture = models.CharField(max_length=100, null=True)
    number_of_shares = models.IntegerField()
    country = models.CharField(max_length=50)
    currency = models.CharField(max_length=30, default='dollar')

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return f"{self.name} - {self.ticker}"

class Stocks(models.Model):
    time = models.DateTimeField(primary_key=True, auto_now_add=True)
    price = models.FloatField()
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    change_percent = models.FloatField()

class User(AbstractUser):
    status = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.username}"

class Portfolio(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    number_of_shares = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Portfolio'

    
class Operations(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    number_of_shares = models.IntegerField(default=0)
    price = models.FloatField()
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Operations'
