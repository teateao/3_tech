import os
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from typing import Any, Optional
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.validators import UnicodeUsernameValidator

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender: str, instance: Optional['User'] = None, created: bool = False, **kwargs: Any) -> None:
    if created and instance is not None:
        # トークンの作成と紐付け
        Token.objects.create(user=instance)
    def __str__(self):
        return self

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Emailを入力して下さい')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=Trueである必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=Trueである必要があります。')
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_('username'), max_length=25, validators=[
                                username_validator], blank=True)
    email = models.EmailField(_('email_address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    def __str__(self):
        return f"{self.username},{self.password},{self.email}"

class Article(models.Model):
    title = models.CharField(max_length=200)
    numbers = models.CharField(max_length=200)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seikaku = models.CharField(max_length=10,default="null,null")
    # def __str__(self):
    #     return f"{self.title}"