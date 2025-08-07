from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image

# Load model once
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_image_embedding(image):
    if hasattr(image, 'read'): 
        image = Image.open(image).convert("RGB")
    else: 
        image = Image.open(image).convert("RGB")
    
    inputs = processor(images=image, return_tensors="pt")
   
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
    
    embedding = image_features.squeeze().numpy().tolist()
    return embedding