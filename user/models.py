from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class LowercaseEmailField(models.EmailField):
    """
    Override the default EmailField to lowercase the email address before
    saving (and thus avoid duplicate case sensitive emails).
    """

    def to_python(self, value):
        value = super().to_python(value)

        return value.lower() if isinstance(value, str) else value


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model.

    by default django uses a username as unique and login key for a user profile. In most of our projects we do not
    want this, we want to login with an e-mail adress instead of a username.

    For more information visit:
    https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#substituting-a-custom-user-model
    https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username
    """

    username = None
    email = LowercaseEmailField(verbose_name=_('Adresse email'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
