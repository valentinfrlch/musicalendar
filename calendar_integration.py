# import google calendar API
import spotify_integration as spot

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def init():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '.secrets/calendar/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)




def create_event(event):
    title = event[0]
    artist = event[1]
    timestamp = event[2]
    # convert timestamp to date, remove time
    timestamp = timestamp.split("T")[0]
    
    event = {
        'summary': title + " by " + artist,
        'description': 'You liked {title} by {artist} on Spotify'.format(title=title, artist=artist),
        'start': {
            'date': timestamp,
            'timeZone': 'Europe/Zurich',
        },
        'end': {
            'date': '2015-05-28T17:00:00-07:00',
            'timeZone': 'Europe/Zurich',
        },
    }
    service = build('calendar', 'v3', credentials=creds)
    event = service.events().insert(calendarId='primary', body=event).execute()    



def main(events):
    for event in events:
        print(event)
    
        
# main(spot.main())

init()