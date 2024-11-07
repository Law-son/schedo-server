import cloudinary
import cloudinary.uploader
import cloudinary.api
import re
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure your Cloudinary credentials here
cloudinary.config(
    cloud_name=os.getenv("cloud_name"),
    api_key=os.getenv("api_key"),
    api_secret=os.getenv("api_secret")
)

class CloudinaryService:
    def __init__(self):
        try:
            # Test the Cloudinary configuration to confirm it's valid
            cloudinary.api.ping()
            print("Cloudinary service initialized successfully")
        except Exception as e:
            print(f"Error initializing Cloudinary service: {e}")

    def upload_file(self, file_name, file_data):
        """
        Upload a file to Cloudinary and return the file's public ID and URL.
        
        Args:
            file_name (str): The name of the file to upload.
            file_data (bytes): The binary data of the file.
        
        Returns:
            dict: A dictionary containing the file's 'public_id' and 'url' if successful.
        """
        try:
            print("Uploading file to Cloudinary...")
            upload_result = cloudinary.uploader.upload(
                file_data,
                public_id=os.path.splitext(file_name)[0],  # Use file name without extension
                resource_type="image"  # Adjust if uploading non-image files
            )
            print("File uploaded successfully:", upload_result)
            
            # Returning both public_id (for file management) and URL (for accessing the file)
            return {
                'public_id': upload_result.get('public_id'),
                'url': upload_result.get('secure_url')
            }
        except Exception as e:
            print(f"An error occurred during upload: {e}")
            return None

    def delete_file(self, file_url):
        """
        Delete a file from Cloudinary using its URL.
        
        Args:
            file_url (str): The URL of the file to delete.
        
        Returns:
            bool: True if the file was deleted successfully, False otherwise.
        """
        try:
            # Extract the public ID from the Cloudinary URL
            # Regex to capture the public ID, which is the last part before the file extension
            match = re.search(r"/upload/v\d+/(.+)\.\w+$", file_url)
            if match:
                public_id = match.group(1)
                print(f"Extracted public ID: {public_id}")
                
                # Delete the file using Cloudinary's destroy method
                cloudinary.uploader.destroy(public_id)
                print("File deleted successfully")
                return True
            else:
                print("Failed to extract public ID from URL.")
                return False
        except Exception as e:
            print(f"An error occurred while deleting the file: {e}")
            return False
