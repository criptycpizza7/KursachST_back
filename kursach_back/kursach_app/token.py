from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainSerializer(TokenObtainPairSerializer):
    
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['is_staff'] = user.is_staff
        # ...

        return token