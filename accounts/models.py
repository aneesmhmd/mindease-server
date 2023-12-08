from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('role') != 'admin':
            raise ValueError('Superuser field role must be "admin"')
        
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser field is_active must be true')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser field is_staff must be true')

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser field is_admin must be True')

        return self.create_user(email=email, password=password, **extra_fields)


class Account(AbstractBaseUser):

    ROLE_CHOICES = (
        ('user', 'user'),
        ('counselor', 'counselor'),
        ('admin', 'admin')
    )

    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.PositiveBigIntegerField(null=True, blank=True)
    role = models.CharField(
        max_length=30, default='user', choices=ROLE_CHOICES)
    profile_image = models.ImageField(
        upload_to='profile_image', null=True, blank=True)

    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_google = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
