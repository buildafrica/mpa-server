from django.db import models
from django.conf import settings
from datetime import datetime, date
# Create your models here.

class PhysicalDescription(models.Model):
    name = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Case(models.Model):
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)
    date_missing = models.DateTimeField(auto_now_add=False)
    missing_from = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(auto_now_add=False)
    physical_description = models.ManyToManyField(PhysicalDescription, through = 'PhysicalDescriptionValue')
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='case_reporter', on_delete=models.CASCADE, blank=True, null=True)
    handler = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='case_handler', blank=True, null=True, on_delete=models.CASCADE)


    # get the url for the dp
    def get_dp_url(self):
        return self.image

    def get_age(self):
        today = date.today()
        dob = self.dob

        age = today.year - dob.year
        if today.month < dob.month or today.month == dob.month and today.day < dob.day:
             age -= 1

        return age

    def __str__(self):
        return self.full_name

class PhysicalDescriptionValue(models.Model):
    physical = models.ForeignKey(PhysicalDescription, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)

class Sighting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sighting_reporter', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=1000)
    send_to_police = models.BooleanField(default=True)
    contact_me = models.BooleanField(default=True)
    missing_case = models.ForeignKey(Case, related_name='missing_case', on_delete=models.CASCADE)
    last_seen_from = models.CharField(max_length=100)
    last_seen_date = models.DateTimeField(auto_now_add=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.last_seen_from

class FAQ(models.Model):
    question = models.CharField(max_length=1000)
    answer = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class AboutUs(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Team(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    dp = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name

        # get the url for the dp
    def get_dp_url(self):
        return self.dp

class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title