from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from models import User
from serializers import UserRegistrationSerializer
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from models import Profile

# Create your views here.

class Userview(APIView):

    def get(self,request):
        user=Profile.objects.all()
        serializer=UserRegistrationSerializer(user,many=True)
        return Response(serializer.data)


    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
