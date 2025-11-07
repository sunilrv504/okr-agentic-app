#!/usr/bin/env python3
"""Test script for Gemini API debugging"""

import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {API_KEY[:10]}..." if API_KEY else "No API key found")

# Test different endpoint formats
endpoints = [
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
    "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent", 
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
]

# Test payload format
payload = {
    "contents": [
        {
            "parts": [
                {"text": "Hello, respond with just the word: SUCCESS"}
            ]
        }
    ],
    "generationConfig": {
        "maxOutputTokens": 50,
        "temperature": 0.1
    }
}

headers = {
    "x-goog-api-key": API_KEY,
    "Content-Type": "application/json"
}

print("\nTesting Gemini API endpoints...")

for i, endpoint in enumerate(endpoints, 1):
    print(f"\n{i}. Testing: {endpoint}")
    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(endpoint, json=payload, headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Success! Response: {json.dumps(data, indent=2)}")
                break
            else:
                print(f"   Error: {response.text[:200]}")
    except Exception as e:
        print(f"   Exception: {str(e)}")

print("\nAPI test completed.")