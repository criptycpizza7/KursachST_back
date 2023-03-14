from django.forms import model_to_dict
from django.shortcuts import render
from .models import Company, Operations, Portfolio, User, Stocks
from .serializers import CompanySerializer, OperationsSerializer, PortfolioSerializer, UserSerializer, UserSerializerProd
from rest_framework import views, viewsets
from rest_framework.response import Response
from datetime import date
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializerProd


class CompanyAPIview(views.APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

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

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        portfolio = Portfolio.objects.filter(user_id=request.data['user_id'])
        if portfolio.exists():
            return Response({'response': portfolio.values()})
        else:
            return Response({'error': 'Неверно указан id пользователя'})
        
    def post(self, request):

        user_portfolio = 0

        try:
            user_portfolio = Portfolio.objects.get(user_id = request.data['user'], company_id = request.data['company'])
            
            serializer = PortfolioSerializer(data=model_to_dict(user_portfolio))
            serializer.is_valid(raise_exception=True)

            valid_user_portfolio = {}
            valid_user_portfolio['id'] = user_portfolio.pk
            valid_user_portfolio['user'] = user_portfolio.user_id
            valid_user_portfolio['company'] = user_portfolio.company_id
            valid_user_portfolio['number_of_shares'] = user_portfolio.number_of_shares

            if valid_user_portfolio['number_of_shares'] + request.data['number_of_shares'] < 0:
                return Response({'error': 'недостаточно акиций для совершения операции'})

            valid_user_portfolio['number_of_shares'] += request.data['number_of_shares']

            if valid_user_portfolio['number_of_shares'] == 0:
                user_portfolio.delete()
                return Response({'response': 'Запись удалена'})

            valid_user_portfolio['user'] = user_portfolio.user
            valid_user_portfolio['company'] = user_portfolio.company

            serializer.update(instance=user_portfolio, validated_data=valid_user_portfolio)

        except:
            user = User.objects.filter(pk = request.data['user'])
            company = Company.objects.filter(pk = request.data['company'])

            if not user.exists():
                return Response({'error': 'Неверный id пользователя'})
            if not company.exists():
                return Response({'error': 'Неверный id компании'})
            
            if request.data['number_of_shares'] < 0:
                return Response({'error': 'У пользователя нет данных акций'})

            serializer = PortfolioSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        current_price = Stocks.objects.filter(company = request.data['company']).latest().price
            
        operation_obj = {'user': request.data['user'], 'company': request.data['company'],
                            'number_of_shares': request.data['number_of_shares'], 'price': current_price,
                            'status': request.data['number_of_shares'] > 0}
        
        operation_serializer = OperationsSerializer(data=operation_obj)
        operation_serializer.is_valid(raise_exception=True)
        operation_serializer.save()

        return Response({'response': serializer.data})
    
class GetOperations(views.APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        operations = Operations.objects.filter(user_id = request.data['user'])
        if operations.exists():
            return Response({'response': operations.values()})
        else:
            try: 
                user = User.objects.get(pk = request.data['user'])
                return Response({'error': 'У пользователя нет операций'})
            except:
                return Response({'error': 'Неверный id пользователя'})