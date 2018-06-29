from rest_framework import serializers
from users.models import PCUser
from users.serializers import UserSerializer
from .models import *
from django.contrib.auth import get_user_model


class CaseSerializer(serializers.ModelSerializer):
     case_reporter = UserSerializer(many=False)
     case_handler = UserSerializer(many=False)
     class Meta:
        model = Case
        fields = ('id', 
        'first_name',
         'surname', 
        #  'image',
          'date_missing', 'missing_from', 'dob', 'sex', 'hair_color', 'eye_color', 'height', 'weight', 'bio', 'case_reporter', 'case_handler',)

class SightingSerializer(serializers.ModelSerializer):
    sighting_reporter = UserSerializer(many=False)
    missing_case = CaseSerializer(many=False)
    class Meta:
        model = Sighting
        fields = ('id', 'name', 'email','phone_number','address', 'send_to_police', 'sighting_reporter', 'contact_me', 'missing_case', 'last_seen_date', 'last_seen_from',)

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer',)

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ('id', 'title', 'content',)

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'position', 'bio', 
        # 'dp',
        )

class PrivacyPolicySerializer(serializers.ModelSerializer): 
    class Meta:
        model = PrivacyPolicy
        fields = ('id', 'title', 'conttent',)

# from rest_framework import serializers
# from . models import * 

# class LanguageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Language
#         fields = ('id', 'name', 'content')