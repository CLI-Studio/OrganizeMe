from datetime import datetime, timezone
from typing import List, Dict, Optional

from googleapiclient.discovery import Resource


def get_future_events(service: Resource) -> List[Dict]:
    """
    Fetches the next 10 upcoming events from the user's primary Google Calendar.

    :param service: Authorized Google Calendar API service instance.
    :return: A list of dictionaries containing event details.
    """
    now = datetime.now(timezone.utc).isoformat()  # Ensures UTC timezone
    print("Getting the upcoming 10 events")

    try:
        # Requesting future events sorted by start time
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=3,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])
    except Exception as error:
        print(f"An error occurred: {error}")
        return []


def display(events: List[Dict]) -> None:
    """
    Displays the start time and summary of each event.

    :param events: A list of dictionaries containing event details.
    """
    if not events:
        print("No upcoming events found.")
        return

    for event in events:
        # Prints the start and name of each upcoming event
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])


def delete_event(service: Resource, event_id: str) -> None:
    """
    Deletes an event from the user's primary Google Calendar.

    :param service: Authorized Google Calendar API service instance.
    :param event_id: The ID of the event to be deleted.
    """
    service.events().delete(calendarId="primary", eventId=event_id).execute()


# event dictionary keys: 'summary', 'location', 'description', 'start', 'end', 'attendees', 'reminders'
def add_event(service: Resource, event: Dict) -> None:
    """
    Adds an event to the user's primary Google Calendar.

    :param service: Authorized Google Calendar API service instance.
    :param event: A dictionary containing event details.
    """
    if not event:
        raise ValueError("Event dictionary is required.")
    service.events().insert(calendarId="primary", body=event).execute()


def create_event(title: Optional[str], start_time: Optional[datetime],
                 end_time: Optional[datetime], description: Optional[str]) -> Dict:
    """
    Creates an event dictionary.
    :param title:
    :param start_time:
    :param end_time:
    :param description:
    :return: A dictionary containing event details fits the Google Calendar API.
    """
    start = {
        "dateTime": start_time.isoformat(),
        "timeZone": "America/Los_Angeles",
    }
    end = {
        "dateTime": end_time.isoformat(),
        "timeZone": "America/Los_Angeles",
    }
    return {
        'summary': title,
        'description': description,
        'start': start,
        'end': end,
    }


def update_event(service: Resource, event_id: str, updated_event: Dict) -> None:
    """
    Updates an event on the user's primary Google Calendar.

    :param service: Authorized Google Calendar API service instance.
    :param event_id: The ID of the event to be updated.
    :param updated_event: A dictionary containing updated event details.
    """
    service.events().update(calendarId="primary", eventId=event_id, body=updated_event).execute()