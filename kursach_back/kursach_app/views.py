from django.forms import model_to_dict
from django.shortcuts import render
from .models import Company, Operations, Portfolio, User, Stocks
from .serializers import CompanySerializer, OperationsSerializer, PortfolioSerializer, UserSerializer, UserSerializerProd
from rest_framework import views, viewsets
from rest_framework.response import Response
from datetime import date
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
import jwt


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializerProd


class RegisterView(views.APIView):

    def post(self, request):

        obj = False
        
        try:
            obj = User.objects.get(username=request.data['username'])
        except:
            pass
        if bool(obj):
            return Response({'error': 'Пользователь с таким логином уже существует'})
        
        try:
            obj = User.objects.get(email=request.data['email'])
        except:
            pass
        if bool(obj):
            return Response({'error': 'Пользователь с такой почтой уже существует'})
        
        try:
            obj = User.objects.get(passport=request.data['passport'])
        except:
            pass
        if bool(obj):
            return Response({'error': 'Пользователь с таким номером паспорта уже существует'})
        
        try:
            obj = User.objects.get(INN=request.data['INN'])
        except:
            pass
        if bool(obj):
            return Response({'error': 'Пользователь с таким ИНН уже существует'})
        
        try:
            obj = User.objects.get(phone_number=request.data['phone_number'])
        except:
            pass
        if bool(obj):
            return Response({'error': 'Пользователь с таким номером телефона уже существует'})
        
        serializer = UserSerializerProd(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(username=request.data['username'],
                                        password=request.data['password'],

                                        first_name=request.data['first_name'],
                                        last_name=request.data['last_name'],
                                        middle_name=request.data['middle_name'],

                                        email=request.data['email'],
                                        INN=request.data['INN'],
                                        passport=request.data['passport'],
                                        phone_number=request.data['phone_number'])

        return Response({'response': serializer.data})


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
    
    
# TODO методы доступны только менеджерам
class SingleCompanyApiView(views.APIView):
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Неверный объект'})
        
        try: 
            instance = Company.objects.get(pk=pk)
            return Response({'response': model_to_dict(instance)})
        except:
            return Response({'error': 'Неверный объект'})

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


class GetStocksByCompany(views.APIView): # для построения графиков
    def get(self, request):
        company = Company.objects.filter(name=request.data['name'])
        if company.exists():
            company_id = company.values()[0]['id']
            stocks = Stocks.objects.filter(company_id=company_id)
            return Response({'response': {'name': company.values()[0]['name'], 'stocks': stocks.values()}})
        else:
            return Response({'error': 'Неверно указано название компании'})
        

# TODO получать user_id из токена
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
        token = request.META['HTTP_AUTHORIZATION'][6:]
        user = jwt.decode(token, key='django-insecure-v96(ul6q_=kr!kmcj-rpu5@0n0&pa^0q&r$mtb1t9-4zwrhstn', algorithms='HS256')['user_id']
        operations = Operations.objects.filter(user_id = user)
        if operations.exists():
            return Response({'response': operations.values()})
        else:
            try: 
                user = User.objects.get(pk = request.data['user'])
                return Response({'error': 'У пользователя нет операций'})
            except:
                return Response({'error': 'Неверный id пользователя'})