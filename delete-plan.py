import os
import requests
from dotenv import load_dotenv

# 1. SETUP
load_dotenv()
API_KEY = os.getenv("INTERVALS_API_KEY")
ATHLETE_ID = os.getenv("INTERVALS_ATHLETE_ID")
AUTH = ('API_KEY', API_KEY)
BASE_URL = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/events"

# Set the date range for the events you wan t to delete
START_DATE = "2026-01-18"
END_DATE = "2026-04-15"

def nuke_workouts():
    print(f"🔍 Searching for workouts to delete between {START_DATE} and {END_DATE}...")
    
    # Fetch events in range
    params = {"oldest": START_DATE, "newest": END_DATE}
    response = requests.get(BASE_URL, params=params, auth=AUTH)
    
    if response.status_code != 200:
        print(f"❌ Error fetching events: {response.status_code}")
        return

    events = response.json()
    # We only want to delete planned workouts, not notes or actual recorded activities
    to_delete = [e for e in events if e.get('category') == 'WORKOUT']

    if not to_delete:
        print("✅ No planned workouts found in this range. Your calendar is already clean!")
        return

    print(f"⚠️ Found {len(to_delete)} workouts. Starting deletion...")

    for event in to_delete:
        event_id = event['id']
        name = event.get('name', 'Unnamed')
        date = event.get('start_date_local', '')[:10]
        
        del_resp = requests.delete(f"{BASE_URL}/{event_id}", auth=AUTH)
        
        if del_resp.status_code in [200, 204]:
            print(f"🗑️ Deleted: {name} ({date})")
        else:
            print(f"❌ Failed to delete {name}: {del_resp.status_code}")

    print("\n✨ Cleanup complete. Your calendar is ready for the fresh import!")

if __name__ == "__main__":
    confirm = input(f"ARE YOU SURE? This will delete all PLANNED workouts from {START_DATE} to {END_DATE}. (y/n): ")
    if confirm.lower() == 'y':
        nuke_workouts()
    else:
        print("Aborted.")
