from langchain_core.tools import tool
import logging
from .spotify_controller import sc

logger = logging.getLogger(__name__)

@tool
def pause():
    """Pause the current Spotify playback."""
    logger.info("Calling tool: pause")
    sc.pause()
    
@tool
def resume():
    """Resume Spotify playback if it was paused."""
    logger.info("Calling tool: resume")
    sc.resume()
    
@tool
def next_track():
    """Skip to the next track in the Spotify queue."""
    logger.info("Calling tool: next_track")
    sc.next_track()
    
@tool
def previous_track():
    """Skip to the previous track or restart the current one."""
    logger.info("Calling tool: previous_track")
    sc.previous_track()

@tool    
def get_playlists():
    """Retrieve a list of the user's private playlist names."""
    logger.info("Calling tool: get_playlists")
    return sc.get_my_playlists()

@tool
def play_playlist(playlist_name: str):
    """
    Start playback of a playlist by its name.
    The argument playlist_name is a string containing the playlist's title (e.g., 'python' or 'Worlds').
    """
    logger.info(f"Calling tool: play_playlist (name='{playlist_name}')")
    sc.play_playlist(playlist_name=playlist_name)
    
@tool 
def search_tracks(query: str):
    """
    Search for tracks in Spotify by title, artist, or keywords.
    Returns a list of tracks with their ID, title, artist, and album.
    """
    logger.info(f"Calling tool: search_tracks (query='{query}')")
    return sc.search_tracks(query=query)

@tool
def play_by_id(track_id: str):
    """
    Play a specific Spotify track using its unique ID.
    The argument track_id is a string (e.g., from search results).
    """
    logger.info(f"Calling tool: play_by_id (id='{track_id}')")
    sc.play_by_id(track_id=track_id)
    
    
@tool
def set_repeat(mode: str = "context"):
    """
    Set the repeat mode for the current playback.
    Possible modes: 
    - 'track': repeats the current song indefinitely.
    - 'context': repeats the entire current playlist or album.
    - 'off': disables repeat mode.
    """
    sc.set_repeat(mode=mode)

@tool
def set_shuffle(active: bool = True):
    """
    Enable or disable shuffle mode for the current playback queue.
    The 'active' argument is a boolean: True to shuffle, False to play in order.
    """
    sc.set_shuffle(state=active)
    

    
