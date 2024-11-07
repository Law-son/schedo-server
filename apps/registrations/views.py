from .serializers import AttendeeSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from .serializers import TicketSerializer
from .models import Attendee, Ticket
from apps.events.models import Event
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
import logging
from rest_framework.exceptions import ValidationError
from .email_service import EmailServices
from django.urls import reverse

# Set up logging
logger = logging.getLogger(__name__)

import string
import random

def generate_ticket_code():
    """Generate a random and unique 10-character alphanumeric string."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(10))


@api_view(['POST'])
@authentication_classes([])  # No authentication required for signup
@permission_classes([AllowAny])  # Allow all users to access this view
def create_attendee(request):
    """
    Create a new attendee based on the provided data.
    :param request: The request containing the attendee data
    :return: A JSON response containing the newly created attendee and ticket
    """
    # Extracting data from the request
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    phone_number = request.data.get('phone_number')
    gender = request.data.get('gender')
    event_id = request.data.get('event')

    # Check if email already exists for this event
    if Attendee.objects.filter(email=email, event=event_id).exists():
        return Response(
            {
                'status': 'error',
                'message': 'An attendee with this email already exists.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Initialize the Attendee serializer with the provided data
    serializer = AttendeeSerializer(
        data={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'gender': gender,
            'event': event_id,
        }
    )

    if serializer.is_valid():
        # Save the attendee data
        attendee = serializer.save()
        print("Added Attendee")

        # Fetch the event instance using the event ID
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response(
                {
                    'status': 'error',
                    'message': 'Event with the given ID does not exist.',
                    'event_id': event_id
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate that the event has a valid creator
        if not event.created_by:
            return Response(
                {
                    'status': 'error',
                    'message': 'Event creator (created_by) is missing.',
                    'event_id': event_id
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ticket_code = generate_ticket_code()  # Generate the ticket code
        ticket_serializer = TicketSerializer(
            data={
                'ticket_code': ticket_code,
                'event': event.id,
                'attendee': attendee.id,
                'created_by': event.created_by.id,
                'is_used': False,
                'event_title': event.title,
                'first_name': attendee.first_name,
                'last_name': attendee.last_name
            }
        )

        # Validate and save ticket
        if ticket_serializer.is_valid():
            ticket = ticket_serializer.save()
            print("Added Ticket")

            # Send congratulatory email
            ticket_url = f"http://localhost:5173/ticket/{ticket_code}"
            subject = "Congratulations on Registering for the Event!"
            message = f"Hello {first_name},\nYou have successfully registered for {event.title}.\nYou can view your ticket here: {ticket_url}\n\nThank you for registering!"

            # Attempt to send the email
            email_success = EmailServices.send_email(
                email=email,
                full_name=f"{first_name} {last_name}",
                subject=subject,
                message=message
            )

            if email_success:
                print("Email sent successfully.")
            else:
                print("Failed to send the email.")

            return Response(
                {
                    'status': 'success',
                    'attendee': serializer.data,
                    'ticket': ticket_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'status': 'error',
                    'message': 'Ticket creation failed.',
                    'ticket_errors': ticket_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # Return detailed errors if Attendee validation fails
    return Response(
        {
            'status': 'error',
            'message': 'Attendee data is invalid.',
            'attendee_errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def fetch_attendees(request, event_id):
    """
    Fetch a list of all attendees for the given event.

    :param request: The request containing the event ID
    :param event_id: The ID of the event
    :return: A JSON response containing the list of attendees
    """
    attendees = Attendee.objects.filter(event__id=event_id)
    serializer = AttendeeSerializer(attendees, many=True)
    return Response(
        {
            'status': 'success',
            'attendees': serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@authentication_classes([])  # No authentication required for signup
@permission_classes([AllowAny])  # Allow all users to access this view
def fetch_ticket(request, ticket_code):
    """
    Fetch an attendee's ticket by their ticket_code.

    :param request: The request containing the attendee's ticket_code
    :return: A JSON response containing the attendee's ticket
    """
    if ticket_code is None:
        return Response(
            {'status': 'error', 'message': 'Ticket code is required'},
            status=status.HTTP_200_OK
        )
    try:
        ticket = Ticket.objects.get(ticket_code=ticket_code)
        ticket_serializer = TicketSerializer(ticket)
        if ticket.is_used:
            return Response(
                {'status': 'error', 'message': 'Ticket has been used'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'status': 'success', 'ticket': ticket_serializer.data},
            status=status.HTTP_200_OK
        )
    except Ticket.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Ticket not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def scan_ticket(request, ticket_code):
    """
    Check if an attendee is registered for an event.

    :param request: The request containing the attendee's ticket_code
    :param ticket_code: The ticket code to check
    :return: A JSON response with "Registered" or "Not Registered" status
    """
    if ticket_code is None:
        return Response(
            {'status': 'error', 'message': 'Ticket code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        ticket = Ticket.objects.get(created_by=request.user, ticket_code=ticket_code)
        if ticket.is_used: 
            return Response({'status': 'Ticket used'}, status=status.HTTP_200_OK)
        else:
            ticket.is_used = True
            ticket.save()
            return Response({'status': 'Registered'}, status=status.HTTP_200_OK)
    except Ticket.DoesNotExist:
        return Response({'status': 'Not Registered'}, status=status.HTTP_200_OK)
