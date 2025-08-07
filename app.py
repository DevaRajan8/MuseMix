import streamlit as st
from models.model import get_image_embedding
from database.db import save_image_embedding
import tempfile
import os

st.title("MuseMix - Image to Music")
image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if image is not None:
    st.image(image, caption="Uploaded Image", use_column_width=True)
    embedding = get_image_embedding(image)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(image.getvalue())
        temp_path = tmp_file.name
   
    try:
        doc_id = save_image_embedding(temp_path, embedding)
        st.success(f"Image saved to database with ID: {doc_id}")
        with st.expander("View Image Embedding"):
            st.json(embedding[:10])  # Show first 10 values only
            st.write(f"Total embedding dimensions: {len(embedding)}")
           
    finally:
        os.unlink(temp_path)