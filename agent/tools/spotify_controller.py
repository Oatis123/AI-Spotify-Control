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
    
    def get_current_playback_info(self):
        logger.info("Fetching current playback info")
        playback = self.sp.current_playback()

        if not playback or not playback.get('device'):
            logger.debug("No active playback or device found")
            return None

        device_name = playback['device']['name']
        is_playing = playback.get('is_playing', False)

        if not is_playing or not playback.get('item'):
            return {
                "device": device_name,
                "is_playing": False,
                "track": None,
                "playlist": None,
                "summary": f"Устройство: {device_name}. Сейчас ничего не играет."
            }

        track_name = playback['item']['name']
        artists = ", ".join([artist['name'] for artist in playback['item']['artists']])
        track_full = f"{artists} - {track_name}"

        playlist_name = None
        context = playback.get('context')

        if context and context.get('type') == 'playlist':
            try:
                playlist_info = self.sp.playlist(context['uri'])
                playlist_name = playlist_info.get('name')
            except Exception as e:
                logger.error(f"Failed to fetch playlist info: {e}")

        if playlist_name:
            summary = f"Устройство: {device_name} | Плейлист: {playlist_name} | Трек: {track_full}"
        else:
            summary = f"Устройство: {device_name} | Трек: {track_full}"

        logger.debug(f"Current playback: {summary}")
        
        return {
            "device": device_name,
            "is_playing": True,
            "track": track_full,
            "playlist": playlist_name,
            "summary": summary
        }

    def get_my_playlists(self):
        logger.info("Fetching user playlists")
        results = self.sp.current_user_playlists()
        playlists = [item['name'] for item in results['items']]
        logger.debug(f"Found playlists: {playlists}")
        return playlists

    def play_playlist_by_name(self, playlist_name):
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
                'album': track['album']['name']
            }
            filtered_tracks.append(track_data)
            
        logger.debug(f"Search found {len(filtered_tracks)} tracks")
        return filtered_tracks
    
    def search_playlists(self, query, limit=10):
        logger.info(f"Searching for playlists with query: {query}")
        results = self.sp.search(q=query, limit=limit, type='playlist')
        items = results['playlists']['items']
        print(items)
        filtered_playlists = []
        for playlist in items:
            if playlist is None:
                continue
            track_data = {
                'id': playlist['id'],
                'name': playlist['name'],
                'owner': playlist['owner']['display_name'],
                'description': playlist['description']
            }
            filtered_playlists.append(track_data)
            
        logger.debug(f"Search found {len(filtered_playlists)} tracks")
        return filtered_playlists 

    def search_albums(self, query, limit=10):
        logger.info(f"Searching for albums with query: {query}")
        results = self.sp.search(q=query, limit=limit, type='album')
        items = results['albums']['items']
        filtered_albums = []
        for album in items:
            album_data = {
                'id': album['id'],
                'name': album['name'],
                'artist': album['artists'][0]['name'],
                'release_date': album['release_date']
            }
            filtered_albums.append(album_data)
            
        logger.debug(f"Search found {len(filtered_albums)} albums")
        return filtered_albums   
    
    def play_track_by_id(self, track_id):
        logger.info(f"Playing track with ID: {track_id}")
        device_id = self.get_device_id()
        uri = f"spotify:track:{track_id}" if not track_id.startswith("spotify:") else track_id
        self.sp.start_playback(device_id=device_id, uris=[uri])
        return True
    
    def play_playlist_by_id(self, playlist_id):
        logger.info(f"Playing track with ID: {playlist_id}")
        device_id = self.get_device_id()
        uri = f"spotify:playlist:{playlist_id}" if not playlist_id.startswith("spotify:") else playlist_id
        self.sp.start_playback(device_id=device_id, context_uri=uri)
        return True
        
    def play_album_by_id(self, album_id):
        logger.info(f"Playing album with ID: {album_id}")
        device_id = self.get_device_id()
        uri = f"spotify:album:{album_id}" if not album_id.startswith("spotify:") else album_id
        self.sp.start_playback(device_id=device_id, context_uri=uri)
        return True        

    # def play_specific_track(self, track_name_or_uri):
    #     logger.info(f"Playing specific track: {track_name_or_uri}")
    #     device_id = self.get_device_id()
    #     if not track_name_or_uri.startswith('spotify:track:'):
    #         tracks = self.search_tracks(track_name_or_uri, limit=1)
    #         if not tracks:
    #             logger.warning("Track not found")
    #             return False
    #         uri = f"spotify:track:{tracks[0]['id']}"
    #     else:
    #         uri = track_name_or_uri
    #     self.sp.start_playback(device_id=device_id, uris=[uri])
    #     return True

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
        
sc = SpotifyController()