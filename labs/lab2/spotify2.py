import sys
import spotipy
import spotipy.util as util

username = "Ze Li"
scope = 'user-top-read'
client_id = '6afc715764044bdfa3c4802f4d459eeb'
client_secret = '16e63279613e40a09e46ef75c77807b3'
redirect_uri = 'http://localhost:8888/callback'

token = util.prompt_for_user_token(
    username=username,
    scope=scope,
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri
)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    ranges = ['short_term', 'medium_term', 'long_term']
    
for range in ranges:
    print("range:", range)
    results = sp.current_user_top_tracks(time_range=range, limit=50)
    
    for i, item in enumerate(results['items']):
        print(i, item['name'], '//', item['artists'][0]['name'])
        print()
else:
    print("Can't get token for", username)