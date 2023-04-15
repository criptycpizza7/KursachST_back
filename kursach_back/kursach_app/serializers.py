from rest_framework import serializers
from .models import Operations, User, Company, Stocks, Portfolio


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['last_login', ]


class UserSerializerProd(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'username']
        read_only_fields = ['id', ]
        extra_kwargs = {'password': {'write_only': True}}


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'


class OperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operations
        fields = '__all__'
