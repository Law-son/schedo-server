from django.db import models

# Model class for User
class User(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the user
    email = models.EmailField(unique=True)    # User's email address (must be unique)
    password = models.CharField(max_length=128)  # Hashed password for user authentication
    is_active = models.BooleanField(default=True)  # Indicates if the user account is active
    date_joined = models.DateTimeField(auto_now_add=True)  # Date and time when the user account was created

    def __str__(self):
        return self.email
    
# Model class for User Profile
class Profile(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the associated User model
    first_name = models.CharField(max_length=30)  # User's first name
    last_name = models.CharField(max_length=30)   # User's last name
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # User's contact phone number
    bio = models.TextField(blank=True, null=True)  # Short biography or description of the user
    profile_picture = models.TextField(blank=True, null=True)  # URL/path for the user's profile picture (optional)
    location = models.CharField(max_length=100, blank=True, null=True)  # User's location or address

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

