from rest_framework import serializers
from.models import Profile
from.models import User
###################################

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings







class UserSerializer(serializers.ModelSerializer):


    # user_id = serializers.SerializerMethodField('get_user_id')



    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number', 'age')
    # def get_user_id(self,obj):
    #     return (obj.user_id.id)


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)

    id = serializers.SerializerMethodField('get_user_id')
    def get_user_id(self,obj):
        return (obj.User.id)

    class Meta:
        model = User
        fields = ('email', 'password', 'profile','id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(
            user=user,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            phone_number=profile_data['phone_number'],
            age=profile_data['age'],
            # id=profile_data['id']
            # img=profile_data['img'],
            # img_cover=profile_data['img_cover'],
        )
        return user

# creating user login serializer..................................................#

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)

            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'token': jwt_token,

        }
