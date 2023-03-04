from django.forms import model_to_dict
from django.shortcuts import render
from .models import Company, User, Stocks
from .serializers import CompanySerializer, UserSerializer
from rest_framework import views
from rest_framework.response import Response
from datetime import date

class UserAPIview(views.APIView):
    def get(self, request):
        data = User.objects.all().values()
        return Response(list(data))

    # def post(self, request):
    #     new_obj = User.objects.create(
    #         username = request.data['username'],
    #         password = request.data['password'],
    #         first_name = request.data['first_name'],
    #         last_name = request.data['last_name'],
    #         email = request.data['email'],
    #         is_superuser = False,
    #         is_staff = request.data['is_staff'],
    #         date_joined = date.today(),
    #     )
    


class CompanyAPIview(views.APIView):
    def get(self, request):
        data = Company.objects.all().values()
        return Response(list(data))

    def post(self, request):
        new_obj = Company.objects.create(
            Name = request.data['name'],
            Ticker = request.data['ticker'],
            Picture = request.data['picture'],
            Number_of_shares = request.data['number_of_shares'],
            Country = request.data['country'],
            Currency = request.data['currency'],
        )
        
        return Response({'response': model_to_dict(new_obj)})
    

class GetStocksByCompany(views.APIView):
    def get(self, request):
        company = Company.objects.filter(Name=request.data['name'])
        if company.exists():
            company_id = company.values()[0]['id']
            stocks = Stocks.objects.filter(Company_id=company_id)
            return Response({'name': company.values()[0]['Name'], 'stocks': stocks.values()})
        else:
            return Response('Неверно указано название компании')
