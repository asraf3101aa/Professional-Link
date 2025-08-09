import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser,
    """
    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    contact_number = PhoneNumberField(_('contact number'), unique=True)
    company_name = models.CharField(_('company name'), max_length=100)
    address = models.CharField(_('address'), max_length=100)
    industry = models.CharField(_('industry'), max_length=100)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    REQUIRED_FIELDS = ['email', 'full_name', 'contact_number', 'company_name', 'address', 'industry']
