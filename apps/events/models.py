from django.db import models
from apps.accounts.models import User  # Importing the User model from the accounts app

# Model class for Event
class Event(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the event
    title = models.CharField(max_length=200)  # Title of the event
    online_link = models.CharField(max_length=200, blank=True, null=True)  # Online link for the event, optional
    description = models.TextField()  # Detailed description of the event
    thumbnail = models.TextField(blank=True, null=True)  # URL/path for event's thumbnail (optional)
    start_date = models.CharField(max_length=20)  # Start date of the event
    end_date = models.CharField(max_length=20)  # End date of the event
    start_time = models.CharField(max_length=15)  # Start time of the event
    end_time = models.CharField(max_length=15)  # End time of the event
    location = models.CharField(max_length=255)  # Venue or location of the event
    category = models.CharField(max_length=50)  # Category of the event (e.g., Workshop, Conference)
    meeting_id = models.CharField(max_length=200, null=True, default='000')  # Meeting id from Google Calendar API
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model (the user who created the event)
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time when the event was created
    updated_at = models.DateTimeField(auto_now=True)  # Date and time when the event was last updated
    is_active = models.BooleanField(default=True)  # Indicates if the event is currently active
    is_public = models.BooleanField(default=False)  # Indicates if the event is public
    is_online = models.BooleanField(default=False)  # Indicates if the event is online

    def __str__(self):
        return self.title
    

# Model class for Archive
class Archive(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the event
    title = models.CharField(max_length=200)  # Title of the event
    online_link = models.CharField(max_length=200, blank=True, null=True)  # Online link for the event, optional
    description = models.TextField()  # Detailed description of the event
    thumbnail = models.TextField(blank=True, null=True)  # URL/path for event's thumbnail (optional)
    start_date = models.CharField(max_length=20)  # Start date of the event
    end_date = models.CharField(max_length=20)  # End date of the event
    start_time = models.CharField(max_length=15)  # Start time of the event
    end_time = models.CharField(max_length=15)  # End time of the event
    location = models.CharField(max_length=255)  # Venue or location of the event
    category = models.CharField(max_length=50)  # Category of the event (e.g., Workshop, Conference)
    meeting_id = models.CharField(max_length=200, null=True, default='000')  # Meeting id from Google Calendar API
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model (the user who created the event)
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time when the event was created
    updated_at = models.DateTimeField(auto_now=True)  # Date and time when the event was last updated
    is_active = models.BooleanField(default=True)  # Indicates if the event is currently active
    is_public = models.BooleanField(default=False)  # Indicates if the event is public
    is_online = models.BooleanField(default=False)  # Indicates if the event is online

    def __str__(self):
        return self.title
