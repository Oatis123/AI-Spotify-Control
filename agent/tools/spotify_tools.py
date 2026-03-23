from langchain_core.tools import tool
from .spotify_controller import sc

@tool
def pause():
    """Поставить текущее воспроизведение музыки в Spotify на паузу."""
    sc.pause()
    
@tool
def resume():
    """Продолжить воспроизведение музыки в Spotify, если оно было на паузе."""
    sc.resume()
    
@tool
def next_track():
    """Переключить на следующий трек в очереди Spotify."""
    sc.next_track()
    
@tool
def previous_track():
    """Вернуться к предыдущему треку или начать текущий заново."""
    sc.previous_track()

@tool    
def get_playlists():
    """Получить список названий всех личных плейлистов пользователя."""
    return sc.get_my_playlists()

@tool
def play_playlist(playlist_name: str):
    """
    Запустить воспроизведение плейлиста по его названию.
    Аргумент playlist_name — строка с названием плейлиста (например, 'python' или 'Worlds').
    """
    sc.play_playlist(playlist_name=playlist_name)
    
@tool 
def search_tracks(query: str):
    """
    Поиск песен в Spotify по названию, исполнителю или ключевым словам.
    Возвращает список треков с их ID, названием, артистом и альбомом.
    Полезно вызвать перед тем, как использовать play_by_id.
    """
    return sc.search_tracks(query=query)

@tool
def play_by_id(track_id: str):
    """
    Включить конкретную песню в Spotify, используя её уникальный ID.
    Аргумент track_id — это строка с ID трека (например, из результатов поиска).
    """
    sc.play_by_id(track_id=track_id)
    

    
