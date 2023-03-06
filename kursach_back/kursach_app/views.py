from django.forms import model_to_dict
from django.shortcuts import render
from .models import Company, Portfolio, User, Stocks
from .serializers import CompanySerializer, UserSerializer
from rest_framework import views
from rest_framework.response import Response
from datetime import date

class UserAPIview(views.APIView):
    def get(self, request):
        data = User.objects.all().values()
        return Response(list(data))


class CompanyAPIview(views.APIView):
    def get(self, request):
        data = Company.objects.all()
        return Response({'response': CompanySerializer(data, many=True).data})

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({'response': serializer.data})
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Неверный объект'})

        try: 
            instance = Company.objects.get(pk=pk)
        except:
            return Response({'error': 'Неверный объект'})

        serializer = CompanySerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'response': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Неверный объект'})
        
        try:
            instance = Company.objects.get(pk=pk)
        except:
            return Response({'error': 'Неверный объект'})
        
        instance.delete()
        return Response({'response': ['deleted',]})
    

class GetStocksByCompany(views.APIView):
    def get(self, request):
        company = Company.objects.filter(Name=request.data['name'])
        if company.exists():
            company_id = company.values()[0]['id']
            stocks = Stocks.objects.filter(Company_id=company_id)
            return Response({'response': {'name': company.values()[0]['Name'], 'stocks': stocks.values()}})
        else:
            return Response({'error': 'Неверно указано название компании'})
        

class GetPortfolioOfUser(views.APIView):
    def get(self, request):
        portfolio = Portfolio.objects.filter(user_id=request.data['user_id'])
        if portfolio.exists():
            return Response({'response': portfolio.values()})
        else:
            return Response({'error': 'Неверно указан id'})
        
