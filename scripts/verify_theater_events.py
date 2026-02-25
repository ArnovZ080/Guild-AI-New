import requests
import time
import subprocess
import os

API_BASE = "http://localhost:8000/api/v1"

def test_theater_events():
    print("🚀 Starting Phase 6 Verification: Agent Theater Events")
    
    # 1. Trigger an agent run
    print("\n1. Triggering 'MarketAnalyst' via API...")
    try:
        resp = requests.post(
            f"{API_BASE}/agents/MarketAnalyst/run",
            json={"input_data": {"query": "Verification test"}, "context": {}}
        )
        if resp.status_code != 200:
            print(f"❌ Failed to trigger agent: {resp.status_code} - {resp.text}")
            return
        print("✅ Agent triggered successfully.")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure the FastAPI server is running (npm run dev:api or similar).")
        return

    # 2. Poll for events
    print("\n2. Polling /events endpoint...")
    found_started = False
    found_completed = False
    
    for _ in range(10):
        try:
            resp = requests.get(f"{API_BASE}/agents/events")
            if resp.status_code == 200:
                events = resp.json()
                for evt in events:
                    if evt['agent_id'] == 'MarketAnalyst':
                        if evt['event_type'] == 'started':
                            found_started = True
                        if evt['event_type'] == 'completed':
                            found_completed = True
                
                if found_started and found_completed:
                    break
            else:
                print(f"⚠️ Polling returned {resp.status_code}")
        except Exception as e:
            print(f"⚠️ Polling error: {e}")
            
        time.sleep(1)

    if found_started:
        print("✅ Detected 'STARTED' event for MarketAnalyst.")
    else:
        print("❌ 'STARTED' event not detected.")

    if found_completed:
        print("✅ Detected 'COMPLETED' event for MarketAnalyst.")
    else:
        print("❌ 'COMPLETED' event not detected.")

    if found_started and found_completed:
        print("\n🎉 Phase 6 Verification SUCCESSFUL: End-to-end event stream is functional.")
    else:
        print("\n❌ Phase 6 Verification FAILED.")

if __name__ == "__main__":
    test_theater_events()
