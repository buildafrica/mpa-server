from rest_framework import serializers 
from users.models import *
from django.contrib.auth import get_user_model

class UserLimitedSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='get_full_name')
    class Meta:
        model = get_user_model()
        fields = ('id', 'email',
                  'full_name', )


class UserSerializer(serializers.ModelSerializer):
    # avatar = serializers.ReadOnlyField(source='get_avatar')
    bg_avatar= serializers.ReadOnlyField(source='get_bg_avatar')
    full_name = serializers.ReadOnlyField(source='get_full_name')
    auth_token = serializers.CharField(max_length=500, read_only=True)
 
    class Meta:
        model = get_user_model()
        fields = ('id', 'auth_token', 'email',
                  'first_name', 'last_name', 'full_name',
                #   'avatar',
                  'country',
                #   'location',
                  'phone_number',
                   'created',
                   'is_legal',
                   'bg_avatar',
                #    'date_of_birth',
                ) 


class UserAuthSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(max_length=500, read_only=True)
    # avatar= serializers.ReadOnlyField(source='get_avatar')
    bg_avatar= serializers.ReadOnlyField(source='get_bg_avatar')
    full_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = get_user_model()
        fields = ('id', 'auth_token', 'email',
                  'first_name', 'last_name', 'full_name',
                  'phone_number', 'created',
                  'country',
                #   'avatar',
                  'bg_avatar',
                #   'date_of_birth',
                #   'location',
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
        user = PCUser(
            email=attrs['email'],
            first_name=attrs['first_name'],
            last_name=attrs['last_name'],
        )
        user.set_password(attrs['password'])
        return user