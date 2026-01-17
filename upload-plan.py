import os
import csv
import time
import requests
import difflib
from dotenv import load_dotenv
from dateutil import parser 

load_dotenv()
API_KEY = os.getenv("INTERVALS_API_KEY")
ATHLETE_ID = os.getenv("INTERVALS_ATHLETE_ID")
AUTH = ('API_KEY', API_KEY)
BASE_URL = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/events"

def get_existing_events(start_date, end_date):
    params = {"oldest": start_date, "newest": end_date}
    response = requests.get(BASE_URL, params=params, auth=AUTH)
    if response.status_code == 200:
        return {(e['start_date_local'][:10], e['name']): (e['id'], e.get('description', '')) 
                for e in response.json() if e.get('category') == 'WORKOUT'}
    return {}

def print_diff(old_text, new_text):
    diff = difflib.ndiff(old_text.splitlines(), new_text.splitlines())
    for line in diff:
        if line.startswith('+ '): print(f"    \033[92m{line}\033[0m")
        elif line.startswith('- '): print(f"    \033[91m{line}\033[0m")

def sync_workouts(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found.")
        return

    with open(file_path, mode='r', encoding='utf-8') as f:
        csv_workouts = list(csv.DictReader(f))

    # Fix dates for the range search
    for row in csv_workouts:
        row['date'] = parser.parse(row['date']).strftime('%Y-%m-%d')

    dates = [w['date'] for w in csv_workouts]
    existing = get_existing_events(min(dates), max(dates))

    for row in csv_workouts:
        date, name = row['date'], row['name']
        
        # Clean up formatting: fix literal \n and remove accidental extra quotes
        new_desc = row['description'].replace('\\n', '\n').replace('"', '').strip()
        
        # Clean the workout type (e.g. "Weight Training" -> "WeightTraining")
        workout_type = row['type'].replace(" ", "")
        
        key = (date, name)
        
        # PAYLOAD UPDATED WITH PACE FIXES
        payload = {
            "start_date_local": f"{date}T08:00:00",
            "type": workout_type,
            "name": name,
            "description": new_desc,
            "workout_text": new_desc,  # Triggers the Intervals parser
            "target": "PACE",           # Tells Garmin to use the Pace Gauge
            "category": "WORKOUT"
        }

        if key in existing:
            event_id, old_desc = existing[key]
            if old_desc.strip() != new_desc.strip():
                print(f"🔄 Updating: {name} on {date}")
                print_diff(old_desc, new_desc)
                resp = requests.put(f"{BASE_URL}/{event_id}", json=payload, auth=AUTH)
            else:
                print(f"⏭️  No changes: {name} on {date}")
                continue
        else:
            print(f"🆕 Creating: {name} on {date}")
            resp = requests.post(BASE_URL, json=payload, auth=AUTH)

        if resp.status_code not in [200, 201]:
            print(f"    \033[91m⚠️ ERROR {resp.status_code}: {name} was NOT uploaded.\033[0m")
            try:
                error_msg = resp.json().get('error', resp.text)
                print(f"    Reason: {error_msg}")
            except:
                print(f"    Raw Response: {resp.text}")
        
        time.sleep(0.1)

if __name__ == "__main__":
    sync_workouts('workouts.csv')
