import os
import logging
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

logger = logging.getLogger(__name__)

class SpotifyController:
    def __init__(self, device_name=None):
        logger.info(f"Initializing SpotifyController with device_name='{device_name}'")
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
        logger.debug("Retrieving device ID")
        devices = self.sp.devices()
        if not devices['devices']:
            logger.warning("No devices found")
            return None
        
        if self.preferred_device_name:
            for d in devices['devices']:
                if self.preferred_device_name.lower() in d['name'].lower():
                    logger.debug(f"Found preferred device: {d['name']} ({d['id']})")
                    return d['id']
                    
        for d in devices['devices']:
            if d['is_active']:
                logger.debug(f"Found active device: {d['name']} ({d['id']})")
                return d['id']
            
        device_id = devices['devices'][0]['id']
        logger.debug(f"Falling back to first device: {devices['devices'][0]['name']} ({device_id})")
        return device_id

    def get_my_playlists(self):
        logger.info("Fetching user playlists")
        results = self.sp.current_user_playlists()
        playlists = [item['name'] for item in results['items']]
        logger.debug(f"Found playlists: {playlists}")
        return playlists

    def play_playlist(self, playlist_name):
        logger.info(f"Attempting to play playlist: {playlist_name}")
        device_id = self.get_device_id()
        playlists = self.sp.current_user_playlists()
        for p in playlists['items']:
            if playlist_name.lower() == p['name'].lower():
                logger.info(f"Playing playlist '{p['name']}' on device {device_id}")
                self.sp.start_playback(device_id=device_id, context_uri=p['uri'])
                return True
        logger.warning(f"Playlist '{playlist_name}' not found")
        return False

    def search_tracks(self, query, limit=10):
        logger.info(f"Searching for tracks with query: {query}")
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
            
        logger.debug(f"Search found {len(filtered_tracks)} tracks")
        return filtered_tracks
    
    def play_by_id(self, track_id):
        logger.info(f"Playing track with ID: {track_id}")
        device_id = self.get_device_id()
        uri = f"spotify:track:{track_id}" if not track_id.startswith("spotify:") else track_id
        self.sp.start_playback(device_id=device_id, uris=[uri])
        return True

    def play_search_top_10(self, query):
        logger.info(f"Playing top 10 results for query: {query}")
        tracks = self.search_tracks(query, limit=10)
        if not tracks:
            logger.warning("No tracks found to play")
            return False
        device_id = self.get_device_id()
        uris = [t['uri'] for t in tracks]
        self.sp.start_playback(device_id=device_id, uris=uris)
        return True

    def play_specific_track(self, track_name_or_uri):
        logger.info(f"Playing specific track: {track_name_or_uri}")
        device_id = self.get_device_id()
        if not track_name_or_uri.startswith('spotify:track:'):
            tracks = self.search_tracks(track_name_or_uri, limit=1)
            if not tracks:
                logger.warning("Track not found")
                return False
            uri = f"spotify:track:{tracks[0]['id']}"
        else:
            uri = track_name_or_uri
        self.sp.start_playback(device_id=device_id, uris=[uri])
        return True

    def pause(self):
        logger.info("Pausing playback")
        self.sp.pause_playback(device_id=self.get_device_id())

    def resume(self):
        logger.info("Resuming playback")
        self.sp.start_playback(device_id=self.get_device_id())

    def next_track(self):
        logger.info("Skipping to next track")
        self.sp.next_track(device_id=self.get_device_id())

    def previous_track(self):
        logger.info("Going to previous track")
        self.sp.previous_track(device_id=self.get_device_id())
        
    def set_repeat(self, mode="context"):
        device_id = self.get_device_id()
        self.sp.repeat(state=mode, device_id=device_id)
        return True

    def set_shuffle(self, state=True):
        device_id = self.get_device_id()
        self.sp.shuffle(state=state, device_id=device_id)
        return True
        

sc = SpotifyController(device_name="DESKTOP-PLNF0UP")
