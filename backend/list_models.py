#!/usr/bin/env python3
"""List available Gemini models"""

import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {API_KEY[:10]}..." if API_KEY else "No API key found")

headers = {
    "x-goog-api-key": API_KEY,
    "Content-Type": "application/json"
}

# List available models
list_url = "https://generativelanguage.googleapis.com/v1beta/models"

print(f"\nListing available models from: {list_url}")

try:
    with httpx.Client(timeout=10) as client:
        response = client.get(list_url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nAvailable models:")
            for model in data.get('models', []):
                name = model.get('name', 'Unknown')
                display_name = model.get('displayName', 'No display name')
                supported_methods = model.get('supportedGenerationMethods', [])
                print(f"  - {name}")
                print(f"    Display: {display_name}")
                print(f"    Methods: {', '.join(supported_methods)}")
                print()
        else:
            print(f"Error: {response.text}")
            
except Exception as e:
    print(f"Exception: {str(e)}")