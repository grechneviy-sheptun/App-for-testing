from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'username', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True},  
            'email': {'required': True}, 
        }

    def validate(self, attrs):
        password = attrs.get('password')
        email = attrs.get('email')
        list_of_valid_email = ['gmail.com', 'ukr.net', 'outlook.com']
        last_of_email = email.partition('@')[2]

        if len(password) < 8:
            raise ValueError(_("Password length must be >= 8"))
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("User with this email already exists, please login"))
        
        if last_of_email not in list_of_valid_email:
            raise serializers.ValidationError(_("Enter a valid email"))
        return attrs    
    
    def create(self, validated_data):
        users = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return users


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    email = serializers.EmailField()

    class Meta:
        fields = '__all__'
        model = User

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        request=self.context.get('request')
        user = authenticate(request=request, username=username, password=password, email=email)
        if not user:
            raise serializers.ValidationError(_("Authentification credentials are not valid"))
        tokens = user.token()

        return {
            'access_token': str(tokens.get('access_token')),
            'refresh_token': str(tokens.get('refresh_token'))
        }
    

class PasswordResetSerializerRequest(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        fields=['email']
        
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user_id = user.id
            token = PasswordResetTokenGenerator().make_token(user=user)
            request = self.context.get('request')

            domain = get_current_site(request=request)
            relative_link = reverse('password-reset-confirm', kwargs={'id':user_id, 'token':token})
            abslink = f"http://{domain}{relative_link}"

            email_body = f"For reseting password click {abslink}"
            message = EmailMessage(
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
                subject="Reset password"
                )
            message.send()
        return super().validate(attrs)

    

class PasswordResetSerializerResponse(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['email', 'password', 'token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        token = attrs.get('token')
        user = User.objects.get(email=email)

        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
            raise serializers.ValidationError(_("reset link is invalid or has expired", 401))
        user.set_password(password)
        user.save()

        return user
