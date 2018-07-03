from rest_framework import serializers 
from .models import *
from django.contrib.auth import get_user_model

class UserLimitedSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='get_full_name')
    class Meta:
        model = get_user_model()
        fields = ('id', 'email',
                  'full_name', )


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.URLField(source='get_dp_url')
    full_name = serializers.ReadOnlyField(source='get_full_name')
    auth_token = serializers.CharField(max_length=500, read_only=True)
 
    class Meta:
        model = get_user_model()
        fields = ('id', 'auth_token', 'email',
                  'first_name', 'last_name', 'full_name',
                  'name_of_organisation',
                  'phone_number',
                   'phone_number1',
                   'created',
                   'is_legal',
                    'avatar',
                  ) 


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password',
                  'first_name', 'last_name',
                  'phone_number',  'phone_number1',
                  'name_of_organisation',
                  'avatar',
                  )

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name',)
        write_only_fields = ('password',)

    def restore_object(self, attrs, instance=None):
        """
        Instantiate a new User instance.
        """
        # assert instance is None, 'Cannot update users with CreateUserSerializer'
        user = MPAUser(
            email=attrs['email'],
            first_name=attrs['first_name'],
            last_name=attrs['last_name'],
        )
        user.set_password(attrs['password'])
        return user