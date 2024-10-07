from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        # Create a new event using the given data
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            # Set the created_by field to the currently authenticated user
            serializer.save(created_by=request.user)
            return Response(
                {
                    'status': 'success',
                    'event': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            # Return error response with validation errors
            return Response(
                {
                    'status': 'error',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        # Handle any other errors that might occur
        return Response(
            {
                'status': 'error',
                'errors': [str(e)]
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_public_events(request):
    try:
        # Fetch all events where is_public is True
        public_events = Event.objects.filter(is_public=True)
        # Serialize the queryset
        serializer = EventSerializer(public_events, many=True)
        # Return the serialized data
        return Response({
            'status': 'success',
            'events': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any errors that might occur
        return Response(
            {
                'status': 'error',
                'errors': [str(e)]
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_events(request, user_id):
    try:
        # Fetch events with the given user_id
        user_events = Event.objects.filter(created_by=user_id)
        # Serialize the queryset
        serializer = EventSerializer(user_events, many=True)
        # Return the serialized data
        return Response({
            'status': 'success',
            'events': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any errors that might occur
        return Response(
            {
                'status': 'error',
                'errors': [str(e)]
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_event(request, event_id):
    try:
        # Fetch the event with the given event_id
        event = Event.objects.get(pk=event_id)
        # Serialize the event
        serializer = EventSerializer(event)
        # Return the serialized data
        return Response({
            'status': 'success',
            'event': serializer.data
        }, status=status.HTTP_200_OK)
    except Event.DoesNotExist:
        # Handle the case where the event does not exist
        return Response(
            {
                'status': 'error',
                'message': 'Event with ID {} does not exist'.format(event_id)
            },
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        # Handle any other errors that might occur
        return Response(
            {
                'status': 'error',
                'errors': [str(e)]
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_event(request, event_id):
    try:
        # Get the event with the given ID
        event = Event.objects.get(id=event_id)
        # Check if the authenticated user is the same as the event creator
        if event.created_by != request.user:
            return Response(
                {
                    'status': 'error',
                    'message': 'You are not authorized to edit this event'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        # Update the event using the given data
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': 'success',
                    'event': serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            # Return error response with validation errors
            return Response(
                {
                    'status': 'error',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    except Event.DoesNotExist:
        # Handle the case where the event does not exist
        return Response(
            {
                'status': 'error',
                'message': 'Event with ID {} does not exist'.format(event_id)
            },
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        # Handle any other errors that might occur
        return Response(
            {
                'status': 'error',
                'errors': [str(e)]
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_event(request, event_id):
    try:
        # Get the event with the given ID
        event = Event.objects.get(id=event_id)
        # Check if the authenticated user is the same as the event creator
        if event.created_by != request.user:
            return Response(
                {
                    'status': 'error',
                    'message': 'You are not authorized to delete this event'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        # Delete the event
        event.delete()
        return Response(
            {
                'status': 'success',
                'message': 'Event with ID {} deleted successfully'.format(event_id)
            },
            status=status.HTTP_200_OK
        )
    except Event.DoesNotExist:
        # Handle the case where the event does not exist
        return Response(
            {
                'status': 'error',
                'message': 'Event with ID {} does not exist'.format(event_id)
            },
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        # Handle any other errors that might occur
        return Response(
            {
                'status': 'error',
                'errors': [str(e)]
            },
            status=status.HTTP_400_BAD_REQUEST
        )

