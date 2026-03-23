import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

class SpotifyController:
    def __init__(self, device_name=None):
        scope = (
            "playlist-read-private "
            "user-modify-playback-state "
            "user-read-playback-state "
            "user-library-read"
        )
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
            scope=scope,
            open_browser=True
        ))
        self.preferred_device_name = device_name

    def get_device_id(self):
        devices = self.sp.devices()
        if not devices['devices']:
            return None
        
        if self.preferred_device_name:
            for d in devices['devices']:
                if self.preferred_device_name.lower() in d['name'].lower():
                    return d['id']
                    
        for d in devices['devices']:
            if d['is_active']: return d['id']
            
        return devices['devices'][0]['id']

    def get_my_playlists(self):
        results = self.sp.current_user_playlists()
        return [item['name'] for item in results['items']]

    def play_playlist(self, playlist_name):
        device_id = self.get_device_id()
        playlists = self.sp.current_user_playlists()
        for p in playlists['items']:
            if playlist_name.lower() == p['name'].lower():
                self.sp.start_playback(device_id=device_id, context_uri=p['uri'])
                return True
        return False

    def search_tracks(self, query, limit=10):
        results = self.sp.search(q=query, limit=limit, type='track')
        items = results['tracks']['items']
        
        filtered_tracks = []
        for track in items:
            track_data = {
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name']
            }
            filtered_tracks.append(track_data)
            
        return filtered_tracks
    
    def play_by_id(self, track_id):
        device_id = self.get_device_id()
        uri = f"spotify:track:{track_id}" if not track_id.startswith("spotify:") else track_id
        self.sp.start_playback(device_id=device_id, uris=[uri])
        return True

    def search_tracks(self, query, limit=10):
        results = self.sp.search(q=query, limit=limit, type='track')
        items = results['tracks']['items']
        
        filtered_tracks = []
        for track in items:
            track_data = {
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'duration_ms': track['duration_ms']
            }
            filtered_tracks.append(track_data)
            
        return filtered_tracks

    def play_search_top_10(self, query):
        tracks = self.search_tracks(query, limit=10)
        if not tracks: return False
        device_id = self.get_device_id()
        uris = [t['uri'] for t in tracks]
        self.sp.start_playback(device_id=device_id, uris=uris)
        return True

    def play_specific_track(self, track_name_or_uri):
        device_id = self.get_device_id()
        if not track_name_or_uri.startswith('spotify:track:'):
            tracks = self.search_tracks(track_name_or_uri, limit=1)
            if not tracks: return False
            uri = tracks[0]['uri']
        else:
            uri = track_name_or_uri
        self.sp.start_playback(device_id=device_id, uris=[uri])
        return True

    def pause(self):
        self.sp.pause_playback(device_id=self.get_device_id())

    def resume(self):
        self.sp.start_playback(device_id=self.get_device_id())

    def next_track(self):
        self.sp.next_track(device_id=self.get_device_id())

    def previous_track(self):
        self.sp.previous_track(device_id=self.get_device_id())
        

sc = SpotifyController(device_name="DESKTOP-PLNF0UP")
