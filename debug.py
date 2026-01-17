import os
import requests
import json
import pyperclip
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("INTERVALS_API_KEY")
ATHLETE_ID = os.getenv("INTERVALS_ATHLETE_ID")
AUTH = ('API_KEY', API_KEY)
BASE_URL = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/events"

def run_debug_pace():
    date = "2026-01-20"
    name = "Debug_Pace_Test"
    
    # We use % of Threshold Pace to force the parser to calculate steps
    desc = "- 10m 70% Pace\n- 5m 90% Pace\n- 5m 60% Pace"
    
    payload = {
        "start_date_local": f"{date}T08:00:00",
        "type": "Run",
        "name": name,
        "description": desc,
        "workout_text": desc,
        "category": "WORKOUT",
        "target": "PACE"
    }

    # 1. Clear old data to ensure a fresh parse
    print(f"Checking for existing {name}...")
    params = {"oldest": date, "newest": date}
    existing = requests.get(BASE_URL, params=params, auth=AUTH).json()
    for event in existing:
        if event['name'] == name:
            requests.delete(f"{BASE_URL}/{event['id']}", auth=AUTH)
            print("Deleted old workout.")

    # 2. Upload with Pace target
    print(f"Uploading {name} with PACE target...")
    post_resp = requests.post(BASE_URL, json=payload, auth=AUTH)
    
    if post_resp.status_code in [200, 201]:
        new_id = post_resp.json()['id']
        time.sleep(1) # Give the server a second to parse the zones
        
        # 3. Fetch the final parsed JSON
        get_resp = requests.get(f"{BASE_URL}/{new_id}", auth=AUTH)
        data = get_resp.json()
        
        # 4. Copy to clipboard
        json_text = json.dumps(data, indent=2)
        pyperclip.copy(json_text)
        
        print("\n" + "="*30)
        print("✅ SUCCESS!")
        print("The JSON is now in your clipboard.")
        print("Paste it here for feedback.")
        print("="*30)
    else:
        print(f"❌ Error: {post_resp.status_code}")
        print(post_resp.text)

if __name__ == "__main__":
    run_debug_pace()
