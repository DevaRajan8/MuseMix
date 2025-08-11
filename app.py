import streamlit as st
from models.model import get_image_embedding
from database.db import save_image_embedding
from music.rag_system import MuseMixRAG
import tempfile
import os
import json

# Initialize RAG system
@st.cache_resource
def load_rag_system():
    return MuseMixRAG()

st.set_page_config(page_title="MuseMix AI", page_icon="🎵", layout="wide")

st.title("🎵 MuseMix AI - Multimodal RAG Music Recommender")
st.markdown("*Upload an image and get personalized music recommendations using AI*")

# Sidebar
st.sidebar.markdown("### How it works:")
st.sidebar.markdown("""
1. **Upload** your image
2. **AI analyzes** visual mood
3. **Searches** similar images in database
4. **Finds** matching music from Last.fm
5. **Generates** personalized recommendations
""")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📸 Upload Image")
    image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    user_prompt = st.text_input("Describe the mood you want (optional):", placeholder="e.g., 'I want something upbeat and energetic'")

with col2:
    st.header("🎵 Music Recommendations")
    
    if image is not None:
        # Display uploaded image
        st.image(image, caption="Your Image", use_column_width=True)
        
        # Get embedding
        with st.spinner("Processing image..."):
            embedding = get_image_embedding(image)
            
            # Save to database
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(image.getvalue())
                temp_path = tmp_file.name
            
            try:
                doc_id = save_image_embedding(temp_path, embedding)
                st.success(f"✅ Image saved to database!")
                
                # Run RAG system
                rag_system = load_rag_system()
                
                with st.spinner("🧠 Analyzing mood and finding music..."):
                    results = rag_system.get_music_recommendations(
                        embedding, user_prompt, top_k=3
                    )
                
                if results.get("success"):
                    # Display mood analysis
                    st.subheader("🎨 Visual Mood Analysis")
                    mood = results["mood_analysis"]
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Energy Level", mood.get("energy_level", "unknown"))
                        st.write("**Emotions:**", ", ".join(mood.get("emotions", [])))
                    
                    with col_b:
                        st.write("**Music Moods:**", ", ".join(mood.get("music_moods", [])))
                        st.write("**Genres:**", ", ".join(mood.get("genres", [])))
                    
                    # Display recommendations
                    st.subheader("🎵 Your Personalized Playlist")
                    st.markdown(results["recommendations"])
                    
                    # Show found tracks
                    with st.expander("🔍 View Found Tracks"):
                        for i, track in enumerate(results["music_tracks"][:10], 1):
                            st.write(f"{i}. **{track['artist']}** - {track['title']} `[{track['mood_tag']}]`")
                    
                    # Show similar images
                    with st.expander("🖼️ Similar Images in Database"):
                        for img in results["similar_images"]:
                            st.write(f"📁 {img['image_path']} (similarity: {img['similarity']:.3f})")
                
                else:
                    st.error(f"❌ Error: {results.get('error', 'Unknown error')}")
                
            finally:
                os.unlink(temp_path)
    
    else:
        st.info("👆 Upload an image to get started!")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit, MongoDB, Last.fm API, and Groq AI*")