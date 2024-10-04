from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a 'User' with an email, password, and other fields."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Model class for User
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # Unique identifier for the user
    email = models.EmailField(unique=True)    # User's email address (must be unique)
    password = models.CharField(max_length=128)  # Hashed password for user authentication
    is_active = models.BooleanField(default=True)  # Indicates if the user account is active
    is_staff = models.BooleanField(default=False)  # Indicates if the user can log into the admin site
    date_joined = models.DateTimeField(auto_now_add=True)  # Date and time when the user account was created

    objects = UserManager()  # Assign the custom manager

    USERNAME_FIELD = 'email'  # The field used for authentication
    REQUIRED_FIELDS = []  # Any additional fields required for createsuperuser (leave empty if none)

    # Adding related_name to avoid clashes with built-in User model
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    def __str__(self):
        return self.email


# Model class for User Profile
class Profile(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Link to the associated User model
    first_name = models.CharField(max_length=30)  # User's first name
    last_name = models.CharField(max_length=30)   # User's last name
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # User's contact phone number
    bio = models.TextField(blank=True, null=True)  # Short biography or description of the user
    profile_picture = models.TextField(blank=True, null=True)  # URL/path for the user's profile picture (optional)
    location = models.CharField(max_length=100, blank=True, null=True)  # User's location or address

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
