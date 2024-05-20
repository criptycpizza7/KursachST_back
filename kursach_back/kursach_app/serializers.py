from rest_framework import serializers
from .models import Operations, User, Company, Stocks, Portfolio


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        read_only_fields = ['id', ]



class UserSerializerProd(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id', ]

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if 'password' not in data:
                raise serializers.ValidationError("password is required for POST")
        return data


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


class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = '__all__'