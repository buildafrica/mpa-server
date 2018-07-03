from django.db import models 
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.core.files.storage import default_storage as storage
from datetime import datetime
from rest_framework.authtoken.models import Token

class MPAUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        """ 
        Creates and saves a User with the given email,
        first_name, last_name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name):
        """
        Creates and saves a superuser with the given email, password,
        first_name and last_name.
        """
        user = self.create_user(email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MPAUser(AbstractBaseUser):
    
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    name_of_organisation = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100 )
    phone_number1 = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    is_legal = models.BooleanField(default=False)

    objects = MPAUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


# return '''{} {}'''.format(self.first_name, self.last_name)
    def get_full_name(self):
        # return '{0} {1}'.format(self.first_name, self.last_name)
        return self.first_name+' '+self.last_name

    def get_short_name(self):
        return self.first_name


    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
        # get the url for the dp
    def get_dp_url(self):
        if self.avatar:
            return self.avatar
        else:
            None

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # On Python 3: def __str__(self):
    def __str__(self):
        return self.email

    class Meta:
        ordering = ('id', 'first_name',)
        verbose_name = _('user')
        verbose_name_plural = _('users')    

@receiver(post_save, sender=MPAUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)