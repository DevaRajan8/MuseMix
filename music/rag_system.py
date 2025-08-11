from database.vector_search import find_similar_images, get_image_context
from music.client import LastFMClient
from models.groq_client import GroqMusicRAG
import json

class MuseMixRAG:
    def __init__(self):
        self.lastfm_client = LastFMClient()
        self.groq_rag = GroqMusicRAG()
    
    def get_music_recommendations(self, image_embedding, user_prompt="", top_k=5):
        """
        Complete Multimodal RAG pipeline
        """
        try:
            # Step 1: RETRIEVE - Find similar images
            print("🔍 Finding similar images...")
            similar_images = find_similar_images(image_embedding, top_k=top_k)
            image_context = get_image_context(similar_images)
            
            # Step 2: ANALYZE - Use Groq to analyze mood
            print("🧠 Analyzing mood with Groq AI...")
            mood_analysis = self.groq_rag.analyze_image_mood(image_context, user_prompt)
            
            if "error" in mood_analysis:
                return {"error": mood_analysis["error"]}
            
            # Step 3: RETRIEVE - Get music data based on mood
            print("🎵 Fetching music tracks from Last.fm...")
            music_moods = mood_analysis.get("music_moods", ["happy", "energetic"])
            music_tracks = self.lastfm_client.get_mood_tracks(music_moods, limit=20)
            
            # Step 4: GENERATE - Final recommendations with Groq
            print("✨ Generating personalized recommendations...")
            final_recommendations = self.groq_rag.generate_music_recommendations(
                mood_analysis, music_tracks
            )
            
            return {
                "success": True,
                "similar_images": similar_images,
                "mood_analysis": mood_analysis,
                "music_tracks": music_tracks,
                "recommendations": final_recommendations
            }
            
        except Exception as e:
            return {"error": f"RAG pipeline error: {str(e)}"}

# Test the complete system
if __name__ == "__main__":
    # This would be called with actual image embedding
    print("MuseMix RAG System initialized!")
    print("Ready to process image embeddings and generate music recommendations!")