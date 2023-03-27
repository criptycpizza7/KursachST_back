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
        fields = ['id', 'password', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'middle_name', 'passport', 'INN', 'phone_number']
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

    # def create(self, validated_data):
    #     return Company.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.ticker = validated_data.get('ticker', instance.ticker)
    #     instance.picture = validated_data.get('picture', instance.picture)
    #     instance.number_of_shares = validated_data.get('number_of_shares', instance.number_of_shares)
    #     instance.country = validated_data.get('country', instance.country)
    #     instance.currency = validated_data.get('currency', instance.currency)
        
    #     instance.save()
        
    #     return instance