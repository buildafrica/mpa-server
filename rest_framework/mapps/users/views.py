from django.shortcuts import render
from .serializers import *
from .models import *
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes, list_route
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
    queryset = MPAUser.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Users ~ create Users

        PARAMETERS:

        first_name , last_name, name_of_organisation, phone_number, phone_number1, email, avatar

        """
        
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        name_of_organisation = request.data.get('name_of_organisation', None)
        phone_number = request.data.get('phone_number', None)
        phone_number1 = request.data.get('phone_number1', None)
        email = request.data.get('email', None)
        avatar = request.FILES.get('avatar', None)
        print('avatar', avatar)
        user = MPAUser.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            name_of_organisation=name_of_organisation,
            phone_number=phone_number,
            phone_number1=phone_number1,
            avatar=avatar,
           )
        # user.profile_picture=avatar
        user.save
       
        userSer = UserCreateSerializer(user, context={'request': request}, many=False)
        return Response(userSer.data, status=HTTP_201_CREATED)

    @list_route(methods=['get'])
    def listAll(self, request, *args, **kwargs):
        """
        returns all users who are legal
        """
        myqueryset = MPAUser.objects.filter(is_legal=False)
      
        serializer = UserSerializer(myqueryset, context={'request': request}, many=True)
        return Response({ 'results': serializer.data}, status=HTTP_200_OK)




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

@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    """
    MOBILE - Login will mostly be done at the front end. 

    POST PARAMETERS:

    email = email

    password = password

    """
    email = request.data.get('email', None)
    password = request.data.get('password', None)

    user = authenticate(email=email, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            user = UserSerializer(user)
            return Response(user.data, status=HTTP_200_OK)
        else:
            return Response({'detail': 'This account has been deactivated'}, status=HTTP_404_NOT_FOUND)
    else:
        return Response({'detail': 'Invalid email or password'}, status=HTTP_404_NOT_FOUND)


