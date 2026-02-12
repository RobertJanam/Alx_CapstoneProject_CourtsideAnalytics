from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# have more attributes for my user profile
class CustomUser(AbstractUser):

    # set of roles
    USER_TYPE_CHOICES = (
        ('COACH', 'Coach/Admin'),
        ('PLAYER', 'Player'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='PLAYER',
        verbose_name='User Role'
    )

    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name='Phone Number'
    )

    # make the email field unique
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        error_messages={
            'unique': "A user with that email already exists."
        }
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    class Meta():
        db_table = 'custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['user_type'])
        ]

    USERNAME_FIELD = 'email' # so a user can log in using email
    REQUIRED_FIELDS = ['username', 'user_type'] # username is now extra