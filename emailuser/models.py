from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
    Group, Permission, PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CoextantPermissionsMixin(models.Model):

    """A mixin class to provide fields compatible with Django's ModelBackend
    permissions model, but with different related names so inheritors can
    coexist with the active User model."""

    is_superuser = models.BooleanField(_('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))
    groups = models.ManyToManyField(Group, verbose_name=_('groups'),
        blank=True, help_text=_('The groups this user belongs to. A user will '
                                'get all permissions granted to each of '
                                'his/her group.'),
        related_name="emailuser_set", related_query_name="emailuser")
    user_permissions = models.ManyToManyField(Permission,
        verbose_name=_('user permissions'), blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="emailuser_set", related_query_name="emailuser")

    class Meta:
        abstract = True


permission_mixin = (PermissionsMixin
    if settings.AUTH_USER_MODEL == 'emailuser.User' else CoextantPermissionsMixin)


class User(AbstractBaseUser, permission_mixin):

    """A Django User object with no username, just an email address."""

    email = models.EmailField(_('email address'), max_length=254, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email.split('@', 1)[0]

    def __str__(self):
        return self.email
