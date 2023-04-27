# take the events as input and convert them to ical format

import icalendar
import datetime

def main(events):
    cal = icalendar.Calendar()
    for event in events:
        title = event[0]
        artist = event[1]
        timestamp = event[2]
        # convert to datetime without time
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").date()
        
        
        event = icalendar.Event()
        event.add('summary', title + " by " + artist)
        event.description = 'You liked {title} by {artist} on Spotify'.format(title=title, artist=artist)
        # add the date, the event is all-day
        event.add('dtstart', timestamp)
        event.add('dtend', timestamp)
        cal.add_component(event)
        
    with open('spotify.ics', 'wb') as f:
        f.write(cal.to_ical())
        