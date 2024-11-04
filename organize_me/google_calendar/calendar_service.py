from datetime import datetime

from googleapiclient.errors import HttpError

from organize_me.google_calendar.auth_connection import connect
import organize_me.google_calendar.calendar_events as calendar


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    try:
        service = connect()
        events = calendar.get_future_events(service)
        calendar.display(events)
        event_id = events[0]["id"]
        calendar.delete_event(service, event_id)
        event = calendar.create_event(
            "trying out the API",
            datetime(2024, 11, 5, 10, 0, 0),
            datetime(2024, 11, 7, 12, 0, 0),
            "this is a test event"
        )
        calendar.add_event(service, event)
        event['summary'] = 'Appointment at Somewhere'
        calendar.update_event(service, event["id"], event)
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
