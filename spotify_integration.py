# connect to spotify api

import spotipy
import time
from ical_integration import main as ical_main
from spotipy.oauth2 import SpotifyOAuth


client_id = open(".secrets/spotify/client_id", "r").read()
client_secret = open(".secrets/spotify/client_secret", "r").read()


def liked_songs():
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://127.0.0.1:9090"))

    r = []
    i = 0
    
    while True:
        results = sp.current_user_saved_tracks(limit=50, offset=i*50)
        for idx, item in enumerate(results['items']):
            track = item['track']
            date_added = item['added_at']
            r.append([track['name'], track['artists'][0]['name'], date_added])
        print(len(r))
        if len(results['items']) < 50:
            break
        time.sleep(1)
        i += 1
    
    return r
    

def library():
    # get all playlist in the users library
    scope = "playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://127.0.0.1:9090"))
    
    # get the current user's username
    username = sp.me()['id']
    
    r = []
    
    # get all the playlists in the user's library and get all the songs in them and add their info to r
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            # print current playlist
            print(playlist['name'])
            results = sp.playlist_items(playlist['id'], fields="items.track.name,items.track.artists,items.added_at")
            print(len(results['items']))
            for item in results['items']:
                track = item['track']
                date_added = item['added_at']
                r.append([track['name'], track['artists'][0]['name'], date_added])
    return r
              
            
#-------------------------------HELPERS---------------------------------------

def search(query):
    # search and return the id of the first result
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://127.0.0.1:9090"))
    
    # search for the query
    result = sp.search(query, limit=1, offset=0, type='track', market=None)
    # get the id and return
    return result['tracks']['items'][0]['id']
    
    
def audio_features(id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://127.0.0.1:9090"))
    
    result = sp.audio_features(id)
    return result[0]


def mood_score(danceability, energy):
    """weights are as follows:
    dance: 60%
    energy: 40%
    """
    return danceability * 0.6 + energy * 0.4


def get_mood_fromtrack(query):
    id = search(query)
    features = audio_features(id)
    mood = mood_score(features['danceability'], features['energy'])
    return mood



def get_calendar():
    # add library and liked songs to one list
    r = library() + liked_songs()
    ical_main(r)







get_calendar()

#print(get_mood_fromtrack("Die Alone"))


#if __name__ == "__main__":
#    main()