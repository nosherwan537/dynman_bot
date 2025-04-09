from google.generativeai import list_models, configure
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file
configure(api_key=os.environ["GEMINI_API_KEY"])

models = list_models()
for model in models:
    print(model.name)
