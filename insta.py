import os
import requests
from google.generativeai import GenerativeModel, configure
from instagrapi import Client
from huggingface_hub import InferenceClient
import time
from io import BytesIO
from dotenv import load_dotenv
load_dotenv() 

# Configure APIs
configure(api_key=os.environ["GEMINI_API_KEY"])
IG_USERNAME = os.environ["INSTAGRAM_USERNAME"]
IG_PASSWORD = os.environ["INSTAGRAM_PASSWORD"]
HF_TOKEN = os.environ["HF_TOKEN"]

# Generate caption using Gemini
def generate_caption():
    model = GenerativeModel('gemini-1.5-pro')
    prompt = """Create Instagram caption for Dynman - cowboy AI artist. Use:
    - 2-3 cowboy metaphors
    - 1 AI art term (neural networks, GANs, etc)
    - 3 hashtags like #CyberCowboy 
    Example: "Ropin' in pixels like digital cattle... #NeuralRanch #CodeCorral"
    """
    response = model.generate_content(prompt)
    return response.text

def generate_image(caption):
    try:
        client = InferenceClient(token=HF_TOKEN)
        image = client.text_to_image(
            f"Professional Instagram influencer photo, {caption}, square aspect ratio",
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )
        
        # Convert PIL Image to bytes
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Save image
        with open("post.jpg", "wb") as f:
            f.write(img_byte_arr)
            
        return "post.jpg"

    except Exception as e:
        print(f"Image processing error: {str(e)}")
        return None
        
# Post to Instagram
def post_to_instagram(image_path, caption):
    cl = Client()
    cl.login(IG_USERNAME, IG_PASSWORD)
    cl.photo_upload(image_path, caption)

# Main script
if __name__ == "__main__":
    caption = generate_caption()
    image_path = generate_image(caption)
    
    if image_path:
        post_to_instagram(image_path, caption)
    else:
        print("Failed to create post")