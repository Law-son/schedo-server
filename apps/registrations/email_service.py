import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SERVICE_ID = os.getenv("SERVICE_ID")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
USER_ID = os.getenv("USER_ID")

class EmailServices:
    @staticmethod
    def send_email(email, full_name, subject, message):
        url = "https://api.emailjs.com/api/v1.0/email/send"
        payload = {
            "service_id": SERVICE_ID,
            "template_id": TEMPLATE_ID,
            "user_id": USER_ID,
            "template_params": {
                "to_email": email,
                "from_name": "Schedo",
                "to_name": full_name,
                "reply_to": "buabassahlawson@gmail.com",
                "subject": subject,
                "message": message,
            },
        }
        headers = {
            "origin": "https://maifriend-server.onrender.com/",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print("Email sent successfully:", response.json())
            return True  # Return True indicating success
        except requests.exceptions.RequestException as error:
            print("Failed to send email:", error)
            return False  # Return False indicating failure
