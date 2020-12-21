from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model to define my User model.
    It is based on django AbstractBaseUser and uses PermissionsMixin.
    It inherits `password` and `last_login` from AbstractBaseUser and
    `is_superuser`, `groups` and `user_permissions` from PermissionsMixin.
    """
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=100)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.password:
                raise ValueError('password must be set')

            self.set_password(self.password)

        return super().save(*args, **kwargs)
