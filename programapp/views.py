from rest_framework import status
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserLoginSerializer

#------------------------------------------------------#
# create the endpoint for logging the user
from rest_framework.views import APIView
# #-------------------------------------------------------
from.models import Profile,User
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
            # user_id=User.objects.get(id)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': {
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'age': user_profile.age,
                    'id':user_profile.id,
                    # 'user_id':user_profile.user_id
                    # 'id':user_id.id,

                    }
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)
#







# class UserLoginView(RetrieveAPIView):
#
#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         response = {
#             'success' : 'True','status code' : status.HTTP_200_OK,'message': 'User logged in  successfully',
#             'token' : serializer.data['token'],
#             }
#         status_code = status.HTTP_200_OK
#
#         return Response(response, status=status_code)









class UserRegistrationView(CreateAPIView):

     serializer_class = UserRegistrationSerializer
     permission_classes = (AllowAny,)

     def post(self, request):
         serializer = self.serializer_class(data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         status_code = status.HTTP_201_CREATED
         response = {'success': 'True', 'status code': status_code, 'message': 'User registered  successfully', }

         return Response(response, status=status_code)








# class UserLoginView(RetrieveAPIView):
#
#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         response = {
#             'success' : 'True',
#             'status code' : status.HTTP_200_OK,
#             'message': 'User logged in  successfully',
#             'token' : serializer.data['token'],
#             }
#         status_code = status.HTTP_200_OK
#
#         return Response(response, status=status_code)






class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid()
        # serializer.save()
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token': serializer.data['token'],

        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
