from django.db import models
from django.conf import settings
from datetime import datetime
# Create your models here.

class Case(models.Model):
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    # image = models.ImageField()
    date_missing = models.DateTimeField(auto_now_add=False)
    missing_from = models.CharField(max_length=100)
    dob = models.DateField(auto_now_add=False)
    sex = models.BooleanField(default=True)
    hair_color = models.CharField(max_length=50)
    eye_color = models.CharField(max_length=50)
    height  = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    bio = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='case_reporter', on_delete=models.CASCADE)
    handler = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='case_handler', blank=True, null=True, on_delete=models.CASCADE)

    # return '''{} {}'''.format(self.first_name, self.surname)
    def get_full_name(self):
        # return '{0} {1}'.format(self.first_name, self.surname)
        return self.first_name+' '+self.surname

    def __str__(self):
        return self.get_full_name

class Sighting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sighting_reporter', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=50)
    address = models.TextField()
    send_to_police = models.BooleanField(default=True)
    contact_me = models.BooleanField(default=True)
    missing_case = models.ForeignKey(Case, related_name='missing_case', on_delete=models.CASCADE)
    last_seen_from = models.CharField(max_length=100)
    last_seen_date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.last_seen_from

class FAQ(models.Model):
    question = models.CharField(max_length=1000)
    answer = models.TextField()

    def __str__(self):
        return self.question

class AboutUs(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField()

    def __str__(self):
        return self.title

class Team(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    # dp = models.ImageField()

    def __str__(self):
        return self.name

class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField()

    def __str__(self):
        return self.title

# from django.db import models

# # Create your models here.

# class Language(models.Model):
#     name = models.CharField(max_length=50)
#     content = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name