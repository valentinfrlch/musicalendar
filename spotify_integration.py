# connect to spotify api

import spotipy
import time, os
from ical_integration import main as ical_main
from spotipy.oauth2 import SpotifyOAuth
import datetime
import json


client_id = open(".secrets/spotify/client_id", "r").read()
client_secret = open(".secrets/spotify/client_secret", "r").read()


def liked_songs():
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://127.0.0.1:9090"))

    r = []
    i = 0
    
    print("liked songs")
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
            results = sp.playlist_items(playlist['id'], fields="items.track.name,items.track.artists,items.added_at")
            print(playlist['name'] + " - " + str(len(results['items'])))
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

def save_library():
    r = library() + liked_songs()
    for i in range(len(r)):
        r[i] = r[i][0].replace(",", "") + " " + r[i][1].replace(",", "") + ", " + r[i][2]
    #write all ids to a .txt file called library.txtM use utf-8 encoding
    with open("library.txt", "w", encoding="utf-8") as f:
        for i in r:
            f.write(i + "\n")
    


def get_calendar():
    # add library and liked songs to one list
    r = library() + liked_songs()
    ical_main(r)


def library_to_mood():
    # read the library.txt file and get the mood of each song
    # if it doesnt exist, create it
    if not os.path.exists("library.txt"):
        save_library()
    if os.path.exists("mood_data.json"):
        print("mood_data.json already exists, skipping...")
        return
    # read the file
    f = open("library.txt", "r", encoding="utf-8")
    tracks = f.readlines()
    
    mood_data = {}
    # in the end we want something like this:
    # {'2023-04-05': [0.51, 0.43, 0.78, ...]}
    
    for track in tracks:
        try:
            # print the progress
            i = tracks.index(track)
            track_name = track.split(",")[0].strip()
            track_date = str(track.split(",")[1].replace("\n", "").strip().split("T")[0])
            # check if key exists
            if track_date not in mood_data:
                mood_data[track_date] = [get_mood_fromtrack(track_name)]
                print(str(i) + "/" + str(len(tracks)) + "   created a new key at " + track_date + " with value " + str(mood_data[track_date]))
            else:
                mood_data[track_date].append(get_mood_fromtrack(track_name))
                print(str(i) + "/" + str(len(tracks)) + "   date already exists, added " + str(get_mood_fromtrack(track_name)) + " to " + track_date)
        except Exception as e:
            print(e)
            continue
    
    print("saving to file...")
        
    # save to file
    j = json.dumps(mood_data)
    f = open("mood_data.json","w")
    f.write(j)
    f.close()
        
        

def average_mood():
    # read the mood_data.json file and get the average mood of each day
    # read the json
    f = open("mood_data.json", "r")
    j = json.loads(f.read())
    
    with open("average_mood_data.json", "w") as g:
        g.write("{\n")
        # for each key, get the average of the values
        for date in j:
            islast = True if date == list(j.keys())[-1] else False
            # get the average of list
            avg = sum(j[date]) / len(j[date])
            # write to file
            if islast:
                g.write('"' + date + '": ' + str(avg) + '\n')
            else:
                g.write('"' + date + '": ' + str(avg) + ',\n')
        g.write("}")

        
average_mood()

#print(get_mood_fromtrack("Die Alone"))


#if __name__ == "__main__":
#    pass