import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Define the scopes required for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_email_via_gmail(subject, body, to):
    creds = None
    # Load the credentials from token file or authenticate if not present
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Create the email message
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the email
    message = {'raw': raw}
    service.users().messages().send(userId='me', body=message).execute()
    print("Email sent successfully!")

if __name__ == "__main__":
    load_dotenv()
    recipient = os.environ.get('NOTIFICATION_ADDRESS')
    send_email_via_gmail(
        subject='Gaimin Calendator sync complete.',
        body='',
        to=recipient
    )
