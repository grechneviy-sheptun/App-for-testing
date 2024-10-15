from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import UserSerializer, LoginSerializer, PasswordResetSerializerRequest, PasswordResetSerializerResponse
from .models import User


class UserRegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serizalizer = self.serializer_class(data=request.data)
        if serizalizer.is_valid(raise_exception=True):
            serizalizer.save()
            return Response({'message': 'User register successfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serizalizer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'User login successfully'},
                            status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        

class UserPasswordResetRequestView(APIView):
   serializer_class = PasswordResetSerializerRequest
   def post(self, request):
       serializer = self.serializer_class(data=request.data, context={'request': request})
       serializer.is_valid(raise_exception=True)
       return Response({'message': 'Link for reseting password was sent to your email'},
                       status=status.HTTP_200_OK)
   

class UserPasswordResetConfirmView(APIView):
    def get(self, request, id, token):
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
            raise ValueError({'message': 'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message': 'Credentials are valid'}, status=status.HTTP_202_ACCEPTED)
    

class UserPasswordReset(APIView):
    serializer_class = PasswordResetSerializerResponse
    def patch(self, request):
        serializer = self.serializer_class(dara=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Password reseted successfully'}, status=status.HTTP_200_OK)

        
    
