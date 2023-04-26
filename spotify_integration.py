# connect to spotify api

import spotipy
from spotipy.oauth2 import SpotifyOAuth





def main():
    scope = "user-library-read"
    client_id = open(".secrets/spotify/client_id", "r").read()
    client_secret = open(".secrets/spotify/client_secret", "r").read()

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://127.0.0.1:9090"))

    results = sp.current_user_saved_tracks()
    r = []
    for idx, item in enumerate(results['items']):
        track = item['track']
        date_added = item['added_at']
        r.append([track['name'], track['artists'][0]['name'], date_added])
    return r

print(main())