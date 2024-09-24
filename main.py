import datetime
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up the Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'path/to/credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

class AIProjectAssistant:
    def __init__(self):
        self.calendar_id = 'primary'

    def add_event(self, summary, description, start_time, end_time):
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/New_York',
            },
        }
        event = service.events().insert(calendarId=self.calendar_id, body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")

    def list_events(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId=self.calendar_id, timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    def set_reminder(self, event_id, minutes_before):
        event = service.events().get(calendarId=self.calendar_id, eventId=event_id).execute()
        event['reminders'] = {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': minutes_before},
                {'method': 'popup', 'minutes': minutes_before},
            ],
        }
        updated_event = service.events().update(calendarId=self.calendar_id, eventId=event['id'], body=event).execute()
        print(f"Reminder set for event: {updated_event['summary']}")

def main():
    assistant = AIProjectAssistant()
    print("Welcome to your AI Project Assistant!")
    while True:
        command = input("Enter a command (add, list, remind, exit): ").strip().lower()
        if command == 'add':
            summary = input("Event summary: ")
            description = input("Event description: ")
            start_time = input("Start time (YYYY-MM-DDTHH:MM:SS): ")
            end_time = input("End time (YYYY-MM-DDTHH:MM:SS): ")
            assistant.add_event(summary, description, start_time, end_time)
        elif command == 'list':
            assistant.list_events()
        elif command == 'remind':
            event_id = input("Event ID: ")
            minutes_before = int(input("Minutes before: "))
            assistant.set_reminder(event_id, minutes_before)
        elif command == 'exit':
            print("Goodbye!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
