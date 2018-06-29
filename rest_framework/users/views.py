from django.shortcuts import render
from .serializers import *
from users.models import *
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # model = get_user_model()

    """
    Returns a paginated list of all users
    """
    serializer_class = UserSerializer
    queryset = PCUser.objects.all()

class CurrentUserProfile(APIView):

    def get(self, request, *args, **kwargs):
        """
        USER ~  Retrieve current user

        return fields = (id', 'email', 'first_name', 'last_name',  'avatar',  'created')
        """
        user = request.user
        try:
            user = UserSerializer(user, context={'request': request})
            return Response({'me': user.data}, status=HTTP_200_OK)
        except:
            user = UserSerializer(user)
            return Response(user.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        """
        USER ~  Edit current user

        """

        user = request.user
        profile = request.data
        try:
            serializer = UserSerializer(user, data=profile, partial=True)

            if serializer.is_valid():
                serializer.save()
            return Response({'results': serializer.data}, status=HTTP_200_OK)
        except:
            serializer = UserSerializer(profile, context={'request': request})
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({'detail':'Something is really wrong'}, status=HTTP_400_BAD_REQUEST)

class UserSocialSignUp(APIView):
    model = get_user_model()
    permission_classes = (AllowAny, )

    def post(self, request):

        """
        USER ~ sign up via social login


        PARAMETERS:

        email = email of user

        first_name = first name of User

        last_name = very obvious

        profile_pic_url: url of profile picture

        """

        email = request.data.get('email', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        sm_avatar = request.data.get('sm_avatar', None)
        bg_avatar = request.data.get('bg_avatar', None)

        try:
            user =PCUser.objects.get(email=email)
            user.first_name=first_name
            user.last_name=last_name
            user.sm_avatar=sm_avatar
            user.bg_avatar=bg_avatar
            user.save()
            user = UserAuthSerializer(user)
            return Response(user.data, status=HTTP_200_OK)
        except PCUser.DoesNotExist:
            if email is not None and first_name is not None\
                    and last_name is not None:
                    user = PCUser(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        sm_avatar=sm_avatar,
                        bg_avatar=bg_avatar
                    )

                    user.save()

                    user = UserAuthSerializer(user)

                    return Response(user.data, status=HTTP_201_CREATED)
            else:
                return Response({'detail': 'Please supply required parameters'}, status=HTTP_400_BAD_REQUEST)