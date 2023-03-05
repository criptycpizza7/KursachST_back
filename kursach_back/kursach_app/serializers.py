from rest_framework import serializers
from .models import User, Company, Stocks, Portfolio


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'


class CompanySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=30)
    ticker = serializers.CharField(max_length=5)
    picture = serializers.CharField(max_length=100)
    number_of_shares = serializers.IntegerField()
    country = serializers.CharField(max_length=50)
    currency = serializers.CharField(max_length=30, default='dollar')

    def create(self, validated_data):
        return Company.objects.create(**validated_data)