import os
import requests
from dotenv import load_dotenv

# Load your .env file
load_dotenv()
API_KEY = os.getenv("INTERVALS_API_KEY")
ATHLETE_ID = os.getenv("INTERVALS_ATHLETE_ID")

# Intervals.icu uses Basic Auth
# Username is literally 'API_KEY', Password is your actual key
AUTH = ('API_KEY', API_KEY)

# Use '0' as a shortcut or your actual ATHLETE_ID
URL = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}"

def check_connection():
    print(f"--- Testing Connection for Athlete {ATHLETE_ID} ---")
    try:
        response = requests.get(URL, auth=AUTH)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Connection Successful!")
            print(f"Connected as: {data.get('name')} (ID: {data.get('id')})")
        elif response.status_code == 401:
            print("❌ Error 401: Unauthorized. Check your API Key in .env.")
        elif response.status_code == 404:
            print("❌ Error 404: Athlete not found. Check your Athlete ID in .env.")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ A Python error occurred: {e}")

if __name__ == "__main__":
    check_connection()
