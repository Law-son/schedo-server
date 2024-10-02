from django.db import models
from apps.accounts.models import User  # Importing the User model from the accounts app
from apps.events.models import Event  # Importing the Event model from the events app (optional)

class Notification(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the notification
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model (the recipient of the notification)
    message = models.TextField()  # The notification message
    timestamp = models.DateTimeField(auto_now_add=True)  # Date and time when the notification was created
    is_read = models.BooleanField(default=False)  # Indicates if the notification has been read
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)  # Link to the Event model (optional)

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message[:20]}..."
