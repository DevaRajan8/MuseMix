import requests
import pylast
import json

# Method 1: Simple HTTP request test
def test_lastfm_simple(api_key):
    """Simple test using requests library"""
    print("🔍 Testing Last.fm API with simple HTTP request...")
    
    # Test endpoint: get top artists
    url = "https://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'chart.gettopartists',
        'api_key': api_key,
        'format': 'json',
        'limit': 5
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Key is working!")
            print("\nTop 5 Artists:")
            for i, artist in enumerate(data['artists']['artist'][:5], 1):
                print(f"{i}. {artist['name']} ({artist['playcount']} plays)")
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Exception: {e}")
        return False

# Method 2: Using pylast library
def test_lastfm_pylast(api_key, shared_secret=None):
    """Test using pylast library (more features)"""
    print("\nTesting Last.fm API with pylast library...")
    
    try:
        # Create network object
        network = pylast.LastFMNetwork(
            api_key=api_key,
            api_secret=shared_secret  # Optional for read-only operations
        )
        
        # Test 1: Get top tracks
        print("Getting top tracks...")
        top_tracks = network.get_top_tracks(limit=3)
        print("Top tracks retrieved!")
        for i, track in enumerate(top_tracks, 1):
            print(f"{i}. {track.item.artist} - {track.item.title}")
        
        # Test 2: Search for an artist
        print("\n🔍 Searching for 'The Beatles'...")
        artist = network.get_artist("The Beatles")
        similar = artist.get_similar(limit=3)
        print("✅ Similar artists found!")
        for i, similar_artist in enumerate(similar, 1):
            print(f"{i}. {similar_artist.item.name}")
        
        # Test 3: Get track info
        print("\n🎵 Getting track info for 'Hey Jude'...")
        track = network.get_track("The Beatles", "Hey Jude")
        tags = track.get_top_tags(limit=3)
        print("✅ Track tags retrieved!")
        for tag in tags:
            print(f"   - {tag.item.name}")
            
        return True
        
    except pylast.WSError as e:
        print(f"❌ Last.fm API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

# Test specific music recommendation functions
def test_music_recommendations(api_key):
    """Test functions we'll use for MuseMix"""
    print("\n🎯 Testing MuseMix specific functions...")
    
    try:
        network = pylast.LastFMNetwork(api_key=api_key)
        
        # Test mood-based search using tags
        print("🌟 Searching for 'happy' music...")
        tag = network.get_tag("happy")
        top_tracks = tag.get_top_tracks(limit=5)
        
        print("✅ Happy tracks found!")
        for i, track in enumerate(top_tracks, 1):
            print(f"{i}. {track.item.artist} - {track.item.title}")
        
        # Test getting track features via tags
        print("\n🏷️ Getting tags for a popular song...")
        track = network.get_track("Dua Lipa", "Levitating")
        tags = track.get_top_tags(limit=5)
        
        print("✅ Track mood tags:")
        for tag in tags:
            print(f"   - {tag.item.name} (weight: {tag.weight})")
            
        return True
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

# Main test function
def main():
    print("🎵 Last.fm API Key Tester")
    print("=" * 40)
    
    # Your actual API credentials
    API_KEY = "f3fdd4fb3cb38028d27cad854fd23a04"
    SHARED_SECRET = "eb072301f9081f347e5a4692c8750d67"
    
    if API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  Please replace API_KEY with your actual Last.fm API key!")
        print("\n📋 To get your API key:")
        print("1. Go to: https://www.last.fm/api/account/create")
        print("2. Create an application")
        print("3. Copy your API key and replace it above")
        return
    
    # Run tests
    success_count = 0
    
    if test_lastfm_simple(API_KEY):
        success_count += 1
    
    if test_lastfm_pylast(API_KEY, SHARED_SECRET if SHARED_SECRET != "YOUR_SHARED_SECRET_HERE" else None):
        success_count += 1
    
    if test_music_recommendations(API_KEY):
        success_count += 1
    
    print("\n" + "=" * 40)
    print(f"🏆 Tests completed: {success_count}/3 passed")
    
    if success_count == 3:
        print("All tests passed! Your Last.fm API is ready for MuseMix!")
    elif success_count > 0:
        print("Some tests passed. Check your API key and internet connection.")
    else:
        print("All tests failed. Please check your API key.")

if __name__ == "__main__":
    main()