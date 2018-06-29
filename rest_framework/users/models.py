from django.db import models
# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from datetime import datetime   
# Create your models here. models

class PCUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email,
            password=password,
             first_name=first_name,
            last_name=last_name,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class PCUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100 )
    country = models.CharField(max_length=200)
    # location = models.CharField(max_length=200, default='Sekondi')
    # avatar = models.ImageField()
    sm_avatar = models.URLField(
        blank=True,
        default=None,
        null=True,
        verbose_name=_('Social Media Avatar'),
        max_length=500
    )
    bg_avatar = models.URLField(
        blank=True,
        default=None,
        null=True,
        verbose_name=_('Big Social Media Avatar'),
        max_length=500
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    is_legal = models.BooleanField(default=False)
    # is_staff = models.BooleanField(defaul)
    objects = PCUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email

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

    def get_avatar(self):
        if self.sm_avatar:
            return self.sm_avatar

        else:
            return None

    def get_bg_avatar(self):
        if self.bg_avatar:
            return self.bg_avatar

        else:
            return None

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        ordering = ('id', 'first_name',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

@receiver(post_save, sender=PCUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)