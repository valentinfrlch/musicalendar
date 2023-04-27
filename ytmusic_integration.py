# get liked songs from youtube music API

from ytmusicapi import YTMusic

yt = YTMusic('.secrets/calendar/credentials.json')
playlistId = yt.create_playlist('test', 'test description')
search_results = yt.search('Oasis Wonderwall')
yt.add_playlist_items(playlistId, [search_results[0]['videoId']])