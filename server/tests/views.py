from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TestSerializer


class TestCreateView(APIView):
    serializer_class = TestSerializer
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response({'message': 'Question created successfully'})
