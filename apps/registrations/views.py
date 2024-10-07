from .serializers import AttendeeSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from .serializers import TicketSerializer
from .models import Attendee, Ticket
from apps.events.models import Event

import string
import random

def generate_ticket_code():
    """Generate a random and unique 10-character alphanumeric string."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(10))

@api_view(['POST'])
def create_attendee(request):
    """
    Create a new attendee based on the provided data.

    :param request: The request containing the attendee data
    :return: A JSON response containing the newly created attendee
    """
    serializer = AttendeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Create a new ticket for the attendee
        event = Event.objects.get(id=serializer.data['event'])
        ticket_serializer = TicketSerializer(
            data = {
                'ticket_code': generate_ticket_code(),
                'event': serializer.data['event'],
                'attendee': serializer.data['id'],
                'event_title': event.title,
                'first_name': serializer.data['first_name'],
                'last_name': serializer.data['last_name']
            }
        )
        if ticket_serializer.is_valid():
            ticket_serializer.save()

        return Response(
            {
                'status': 'success',
                'attendee': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {
            'status': 'error',
            'errors': serializer.errors
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
def fetch_ticket(request, ticket_code):
    """
    Fetch an attendee's ticket by their ticket_code.

    :param request: The request containing the attendee's ticket_code
    :return: A JSON response containing the attendee's ticket
    """
    if ticket_code is None:
        return Response(
            {'status': 'error', 'message': 'Ticket code is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        ticket = Ticket.objects.get(ticket_code=ticket_code)
        ticket_serializer = TicketSerializer(ticket)
        if ticket.is_used:
            return Response(
                {'status': 'error', 'message': 'Ticket has been used'},
                status=status.HTTP_400_BAD_REQUEST
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
        ticket = Ticket.objects.get(ticket_code=ticket_code)
        if ticket.is_used:
            return Response({'status': 'Ticket used'}, status=status.HTTP_200_OK)
        else:
            ticket.is_used = True
            ticket.save()
            return Response({'status': 'Registered'}, status=status.HTTP_200_OK)
    except Ticket.DoesNotExist:
        return Response({'status': 'Not Registered'}, status=status.HTTP_200_OK)
