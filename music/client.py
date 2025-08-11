import pylast
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class LastFMClient:
    def __init__(self):
        self.api_key = os.getenv("LASTFM_API_KEY")
        self.shared_secret = os.getenv("LASTFM_SHARED_SECRET")
        self.network = pylast.LastFMNetwork(
            api_key=self.api_key,
            api_secret=self.shared_secret
        )
    
    def get_mood_tracks(self, mood_keywords, limit=10):
        """
        Get tracks based on mood keywords
        """
        all_tracks = []
        
        for mood in mood_keywords:
            try:
                tag = self.network.get_tag(mood)
                tracks = tag.get_top_tracks(limit=limit//len(mood_keywords))
                
                for track in tracks:
                    track_info = {
                        "artist": str(track.item.artist),
                        "title": str(track.item.title),
                        "mood_tag": mood,
                        "playcount": track.weight if hasattr(track, 'weight') else 0
                    }
                    all_tracks.append(track_info)
                    
            except Exception as e:
                print(f"Error fetching tracks for mood '{mood}': {e}")
                continue
        
        return all_tracks
    
    def get_track_tags(self, artist, title, limit=5):
        """
        Get mood/genre tags for a specific track
        """
        try:
            track = self.network.get_track(artist, title)
            tags = track.get_top_tags(limit=limit)
            return [str(tag.item.name) for tag in tags]
        except:
            return []
    
    def get_similar_artists(self, artist_name, limit=5):
        """
        Get similar artists
        """
        try:
            artist = self.network.get_artist(artist_name)
            similar = artist.get_similar(limit=limit)
            return [str(similar_artist.item.name) for similar_artist in similar]
        except:
            return []

# Test the client
if __name__ == "__main__":
    client = LastFMClient()
    print("Testing mood tracks...")
    tracks = client.get_mood_tracks(["happy", "energetic"], limit=5)
    for track in tracks[:3]:
        print(f"- {track['artist']} - {track['title']} [{track['mood_tag']}]")