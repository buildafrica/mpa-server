from rest_framework import serializers
from mapps.users.models import MPAUser
from mapps.users.serializers import UserSerializer
from .models import *
from django.contrib.auth import get_user_model

class PhysicalDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalDescription
        fields = ('id', 'name', 'date_posted',)

class PhysicalDescriptionValueSeralizer(serializers.ModelSerializer):
    physical= PhysicalDescriptionSerializer(many=False)
    class Meta:
        model = PhysicalDescriptionValue
        fields = ('id','physical', 'value')

class CaseSerializer(serializers.ModelSerializer):
    physical_description = PhysicalDescriptionValueSeralizer(source='physicaldescriptionvalue_set',many=True)
    image = serializers.URLField(source='get_dp_url')
    age = serializers.ReadOnlyField(source='get_age')
    user = UserSerializer(many=False)
    handler = UserSerializer(many=False)
    class Meta:
        model = Case
        fields = ('id', 'full_name', 
        'image', 'date_missing', 'missing_from', 'age', 
        'address', 
        'mobile',
        'physical_description', 'description', 
        'user', 'handler', 'date_posted')

class CaseAddSerializer(serializers.ModelSerializer):
    physical_description = PhysicalDescriptionValueSeralizer(source='physicaldescriptionvalue_set',many=True)
    case_reporter = UserSerializer(many=False)
    case_handler = UserSerializer(many=False)
    class Meta:
        model = Case
        fields = ('id', 'full_name', 
        'image', 'date_missing', 'missing_from', 'dob', 
        'address', 
        'moibile',
        'physical_description', 'description', 
        'case_reporter', 'case_handler', 'date_posted')

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
        fields = ('id', 'name', 'position', 'bio', 'dp',)

class PrivacyPolicySerializer(serializers.ModelSerializer): 
    class Meta:
        model = PrivacyPolicy
        fields = ('id', 'title', 'content',)