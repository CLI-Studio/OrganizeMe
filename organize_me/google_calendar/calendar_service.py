from datetime import datetime

from googleapiclient.errors import HttpError    # type: ignore

from organize_me.google_calendar.auth_connection import connect
import organize_me.google_calendar.calendar_events as calendar


def main() -> None:
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.

    Before running this script, make sure you have at lease one event in your primary calendar
    """
    try:
        # Connect to the Google Calendar API
        service = connect()

        # fetch the next 10 upcoming events
        print("Getting the upcoming 10 events")
        future_events = calendar.get_future_events(service)
        calendar.display(future_events)

        # delete the first event
        print("Deleting the first event")
        event_id_to_delete = future_events[0]["id"]
        calendar.delete_event(service, event_id_to_delete)

        # create a new event
        print("Creating a new event")
        example_converting_task_to_event = calendar.create_event(
            "trying out the API",
            datetime(2024, 11, 9, 10, 0, 0),
            datetime(2024, 11, 12, 12, 0, 0),
            "this is a test event"
        )
        calendar.add_event(service, example_converting_task_to_event)

        # fetch the next 10 upcoming events
        print("Getting the upcoming 10 events")
        future_events = calendar.get_future_events(service)
        calendar.display(future_events)

        # edit the first event
        print("Editing the first event")
        event_to_edit = future_events[0]
        event_to_edit['summary'] = 'edited event'
        calendar.update_event(service, event_to_edit["id"], event_to_edit)

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
