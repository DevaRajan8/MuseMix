from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

class GroqMusicRAG:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"  # Or ""
    
    def analyze_image_mood(self, image_context, user_prompt=""):
        system_prompt = """You are MuseMix AI, an expert at connecting visual moods with music recommendations.

Your task:
1. Analyze the visual context provided
2. Extract mood, energy level, emotions, and atmosphere
3. Suggest music genres, moods, and characteristics that match
4. Return response in JSON format

Response format:
{
    "visual_mood": "description of image mood",
    "energy_level": "low/medium/high",
    "emotions": ["emotion1", "emotion2"],
    "music_moods": ["mood1", "mood2", "mood3"],
    "genres": ["genre1", "genre2"],
    "tempo_preference": "slow/medium/fast",
    "atmosphere": "description"
}"""

        user_message = f"""
Image Context: {image_context}
User Input: {user_prompt if user_prompt else "Please analyze this image and suggest matching music"}

Analyze this visual information and provide music recommendations that would match the mood and atmosphere.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            content = response.choices[0].message.content
            try:
                return json.loads(content)
            except:
                # If JSON parsing fails, return structured response
                return {
                    "visual_mood": "Could not parse mood",
                    "raw_response": content
                }
                
        except Exception as e:
            print(f"Groq API Error: {e}")
            return {"error": str(e)}
    
    def generate_music_recommendations(self, mood_analysis, music_tracks):
        system_prompt = """You are MuseMix AI. Create personalized music recommendations based on visual mood analysis and available tracks.

Provide:
1. Top 5-8 track recommendations with explanations
2. Why each track matches the visual mood
3. Brief description of the overall playlist vibe

Be creative and insightful in your explanations."""

        user_message = f"""
Visual Mood Analysis: {json.dumps(mood_analysis, indent=2)}

Available Tracks: {json.dumps(music_tracks[:20], indent=2)}

Create a curated playlist that perfectly matches the visual mood. Explain why each recommendation fits.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Groq API Error: {e}")
            return f"Error generating recommendations: {e}"

if __name__ == "__main__":
    groq_rag = GroqMusicRAG()
    test_context = "Similar images found: sunset, warm colors, peaceful atmosphere"
    result = groq_rag.analyze_image_mood(test_context)
    print("Mood Analysis:", json.dumps(result, indent=2))