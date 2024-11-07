from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Archive
from apps.registrations.models import Attendee
from .serializers import EventSerializer, ArchiveSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from .cloudinary import CloudinaryService  
from django.conf import settings


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        # Parse file from the request
        parser_classes = (MultiPartParser,)

        # print("Request Data:", request.data)
        # print("Request Files:", request.FILES)

        # Check if the thumbnail image is present
        if 'thumbnail' not in request.FILES:
            print("Error: Thumbnail image is required")
            return Response({
                'status': 'error',
                'message': 'Thumbnail image is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get the uploaded image file
        thumbnail = request.FILES['thumbnail']

        # Initialize CloudinaryService
        cloudinary_service = CloudinaryService()

        # Upload the file to Cloudinary and get the file's public ID and URL
        upload_result = cloudinary_service.upload_file(thumbnail.name, thumbnail.read())

        if upload_result:
            # Retrieve the URL to use in your database
            file_link = upload_result['url']
        else:
            print("Failed to upload file to Cloudinary.")

        # Prepare data for the serializer
        data = request.data.copy()

        # Convert string 'true'/'false' to a proper boolean
        data['is_public'] = str(data.get('is_public', 'false')).lower() == 'true'
        data['is_online'] = str(data.get('is_online', 'false')).lower() == 'true'

        # Replace thumbnail with file_link
        data['thumbnail'] = file_link


        # Create the event with the modified data
        serializer = EventSerializer(data=data)
        
        if serializer.is_valid():
            # Save event data (thumbnail is already in data)
            event = serializer.save(created_by=request.user)
            # print("Event Created Successfully:", event)
            return Response({
                'status': 'success',
                'event': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)
            # Handle validation errors
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Log the exception with traceback for better debugging
        import traceback
        print("Exception occurred:", str(e))
        print(traceback.format_exc())
        
        # Handle any exceptions during the process
        return Response({
            'status': 'error',
            'message': 'An error occurred while creating the event. Please try again later.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
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
def get_user_events(request):
    try:
        # Fetch events with the given user_id
        user_events = Event.objects.filter(created_by=request.user)
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
def get_event_attendance(request):
    try:
        # Fetch events created by the authenticated user
        user_events = Event.objects.filter(created_by=request.user)
        
        # Initialize an empty list to store the results
        event_data = []

        # Loop through the fetched events and count the number of attendees for each event
        for event in user_events:
            # Count the number of confirmed attendees for the event
            attendee_count = Attendee.objects.filter(event=event, status='confirmed').count()

            # Append the event data and number of attendees to the result list
            event_data.append({
                'id': event.id,
                'event': event.id,
                'title': event.title,
                'start_date': event.start_date,
                'number_of_attendees': attendee_count
            })

        # Return the result as a response
        return Response({
            'status': 'success',
            'events': event_data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Handle any errors that might occur
        return Response({
            'status': 'error',
            'errors': [str(e)]
        }, status=status.HTTP_400_BAD_REQUEST)


    

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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def archive_event(request, event_id):
    try: 
        # Get the event with the given ID
        event = Event.objects.get(id=event_id)
        # Check if the authenticated user is the same as the event creator
        if event.created_by != request.user:
            return Response(
                {
                    'status': 'error',
                    'message': 'You are not authorized to archive this event'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Create a new instance of the Archive model
        archive = Archive(
            title=event.title,
            description=event.description,
            location=event.location,
            category=event.category,
            meeting_id=event.meeting_id if event.meeting_id else None,
            start_date=event.start_date,
            end_date=event.end_date,
            start_time=event.start_time,
            end_time=event.end_time,
            thumbnail=event.thumbnail,
            is_public=event.is_public,
            is_online=event.is_online,
            created_by=request.user
        )

        # Save the Archive instance
        archive.save()
        print(f"Event {event_id} archived successfully as {archive.id}")

        # Serialize the archived event
        serializer = ArchiveSerializer(archive)

        # Delete the event from the Event table
        event.delete()
        print(f"Event {event_id} deleted after being archived")

        return Response(
            {
                'status': 'success',
                'message': f'Event with ID {event_id} archived successfully',
                'archived_event': serializer.data
            },
            status=status.HTTP_200_OK
        )

    except Event.DoesNotExist:
        print(f"Event with ID {event_id} does not exist")
        return Response(
            {
                'status': 'error',
                'message': f'Event with ID {event_id} does not exist'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        print(f"An error occurred while archiving event {event_id}: {e}")
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
def delete_all_events(request):
    try:
        # Fetch all archived events with the given user_id
        archived_events = Archive.objects.filter(created_by=request.user)
        # Serialize the queryset
        serializer = ArchiveSerializer(archived_events, many=True)
        # Delete all archived events
        archived_events.delete()
        return Response(
            {
                'status': 'success',
                'message': 'All archived events for user with ID {} deleted successfully'.format(request.user.id),
                'deleted_events': serializer.data
            },
            status=status.HTTP_200_OK
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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def restore_all_events(request):
    try:
        # Fetch all archived events with the given user_id
        archived_events = Archive.objects.filter(created_by=request.user)
        # Loop through the events and restore them to the events table
        restored_events = []
        for event in archived_events:
            # Create a new event instance
            new_event = Event(
                title=event.title,
                description=event.description,
                location=event.location,
                category=event.category,
                meeting_id = event.meeting_id if event.meeting_id else None,
                start_date=event.start_date,
                end_date=event.end_date,
                start_time=event.start_time,
                end_time=event.end_time,
                thumbnail=event.thumbnail,
                is_public=event.is_public,
                is_online=event.is_online,
                created_by=request.user
            )
            # Save the new event instance
            new_event.save()
            # Serialize the restored event
            serializer = EventSerializer(new_event)
            restored_events.append(serializer.data)
            # Delete the instance from the Archive table
            event.delete()
        return Response(
            {
                'status': 'success',
                'message': 'All archived events for user with ID {} restored successfully'.format(request.user.id),
                'restored_events': restored_events
            },
            status=status.HTTP_200_OK
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
        # Fetch the event with the given event_id
        event = Archive.objects.get(pk=event_id)
        # Check if the authenticated user is the same as the event creator
        if event.created_by != request.user:
            return Response(
                {
                    'status': 'error',
                    'message': 'You are not authorized to delete this event'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        # Serialize the event before deleting
        event_serializer = EventSerializer(event)

        # Initialize CloudinaryService
        cloudinary_service = CloudinaryService()

        # Upload the file to Cloudinary and get the file's public ID and URL
        cloudinary_image = cloudinary_service.delete_file(event.thumbnail)

        if cloudinary_image:
            print("Image deleted successfully.")
        else:
            print("Failed to upload file to Cloudinary.")

        # Delete the event from the Archive table
        event.delete()
        return Response(
            {
                'status': 'success',
                'message': 'Event with ID {} deleted successfully'.format(event_id),
                'deleted_event': event_serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Archive.DoesNotExist:
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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def restore_event(request, event_id):
    try:
        # Fetch the archived event with the given event_id
        event = Archive.objects.get(pk=event_id)
        # Check if the authenticated user is the same as the event creator
        if event.created_by != request.user:
            return Response(
                {
                    'status': 'error',
                    'message': 'You are not authorized to restore this event'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        # Create a new event instance
        new_event = Event(
            title=event.title,
            description=event.description,
            location=event.location,
            category=event.category,
            meeting_id=event.meeting_id if event.meeting_id else None,
            start_date=event.start_date,
            end_date=event.end_date,
            start_time=event.start_time,
            end_time=event.end_time,
            thumbnail=event.thumbnail,
            is_public=event.is_public,
            is_online=event.is_online,
            created_by=request.user
        )
        # Save the new event instance
        new_event.save()
        # Serialize the new event instance
        serializer = EventSerializer(new_event)
        # Delete the instance from the Archive table
        event.delete()
        return Response(
            {
                'status': 'success',
                'event': serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Archive.DoesNotExist:
        # Handle the case where the event does not exist in the Archive
        return Response(
            {
                'status': 'error',
                'message': 'Event with ID {} does not exist in the archive'.format(event_id)
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

    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_archives(request):
    try:
        # Fetch all archived events with the given user_id
        archived_events = Archive.objects.filter(created_by=request.user)
        # Serialize the queryset
        serializer = EventSerializer(archived_events, many=True)
        # Return the serialized data
        return Response(
            {
                'status': 'success',
                'events': serializer.data
            },
            status=status.HTTP_200_OK
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

