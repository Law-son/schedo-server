from django.db import models
from apps.accounts.models import User  # Importing the User model from the accounts app
from apps.events.models import Event  # Importing the Event model from the events app

# Model class for Attendee
class Attendee(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the attendee
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model (the attendee)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Link to the Event model (the event they are attending)
    registration_date = models.DateTimeField(auto_now_add=True)  # Date and time when the attendee registered
    status = models.CharField(max_length=20, choices=[  # Status of the registration
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled')
    ], default='confirmed')  # Default status set to 'Confirmed'

    def __str__(self):
        return f"{self.user} attending {self.event.title}"
    

# Model class for Ticket
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)  # Unique identifier for the ticket
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Link to the Event model (the event for which the ticket is valid)
    first_name = models.CharField(max_length=100)  # Attendee's first name
    last_name = models.CharField(max_length=100)  # Attendee's last name
    issued_date = models.DateTimeField(auto_now_add=True)  # Date and time when the ticket was issued
    is_used = models.BooleanField(default=False)  # Indicates if the ticket has been used (default is False)

    def __str__(self):
        return f"Ticket for {self.first_name} {self.last_name} to {self.event.title}"
