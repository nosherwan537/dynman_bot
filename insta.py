import os
import requests
from google.generativeai import GenerativeModel, configure
from instagrapi import Client
import time
from dotenv import load_dotenv
load_dotenv() 

# Configure APIs
configure(api_key=os.environ["GEMINI_API_KEY"])
STABILITY_KEY = os.environ["STABILITY_KEY"]
IG_USERNAME = os.environ["INSTAGRAM_USERNAME"]
IG_PASSWORD = os.environ["INSTAGRAM_PASSWORD"]

# Generate caption using Gemini
def generate_caption():
    model = GenerativeModel('gemini-pro')
    prompt = """Create Instagram caption for Dynman - cowboy AI artist. Use:
    - 2-3 cowboy metaphors
    - 1 AI art term (neural networks, GANs, etc)
    - 3 hashtags like #CyberCowboy 
    Example: "Ropin' in pixels like digital cattle... #NeuralRanch #CodeCorral"
    """
    response = model.generate_content(prompt)
    return response.text

# Generate image
def generate_image(caption):
    try:
        API_KEY = os.environ["STABILITY_KEY"]
        url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "image/*"
        }

        data = {
            "prompt": f"professional instagram influencer photo, {caption}",
            "output_format": "jpeg",
            "aspect_ratio": "1:1"
        }

        response = requests.post(url, headers=headers, files={"none": ''}, data=data)
        response.raise_for_status()
        
        # Save image
        with open("post.jpg", "wb") as f:
            f.write(response.content)
            
        return "post.jpg"  # Return local file path

    except Exception as e:
        print(f"Free image error: {str(e)}")
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