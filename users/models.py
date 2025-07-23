from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_type, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))

        email = self.normalize_email(email)
        user = CustomUser(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField(unique=True)
    official_class = models.CharField()
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    USER_TYPE_CHOICES = [
        (0, "Student"),
        (1, "Teacher"),
        (2, "Guidance"),
        (3, "Admin"),
        (4, "Superuser"),
    ]
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.last_name}, {self.first_name}; {self.user_type}"
