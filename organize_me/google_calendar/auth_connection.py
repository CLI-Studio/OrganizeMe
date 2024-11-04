import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Configurations
SCOPES = ["https://www.googleapis.com/auth/calendar"]      # after modifying, delete token.json
TOKEN_FILE = "token.json"                                  # contains user's access
CREDENTIALS_FILE = "credentials.json"                      # contains client_id and client_secret


def save_credentials(creds):
    """Save the credentials for future runs."""
    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())


def user_login(creds=None):
    """
    Manages user login and token refresh.
    :param creds: Existing user credentials, if available
    :return: Updated user credentials
    """
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    save_credentials(creds)
    return creds


def connect():
    """
    Connect to the Google Calendar API, handling user authentication if necessary.
    :return: Authorized Google Calendar API service instance
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        creds = user_login(creds)

    service = build("calendar", "v3", credentials=creds)
    return service


def main():
    """
    Initializes the Google Calendar API connection.
    """
    try:
        connect()
    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    main()
