import requests
import json

BASE_URL = "http://localhost:8001"

def test_waitlist():
    print("Testing Waitlist API...")
    # Join waitlist
    resp = requests.post(f"{BASE_URL}/waitlist/join", json={
        "email": "test@example.com",
        "full_name": "Test User"
    })
    print(f"Join: {resp.status_code} - {resp.json()}")
    
    # Check listing (admin flow)
    resp = requests.get(f"{BASE_URL}/waitlist/list")
    print(f"List: {resp.status_code} - {len(resp.json())} entries")
    
    # Grant access
    resp = requests.post(f"{BASE_URL}/waitlist/grant-beta-access", json={"email": "test@example.com"})
    print(f"Grant: {resp.status_code} - {resp.json()}")
    
    # Verify access
    resp = requests.post(f"{BASE_URL}/waitlist/check-beta-access", json={"email": "test@example.com"})
    print(f"Verify: {resp.status_code} - {resp.json()}")

def test_subscriptions():
    print("\nTesting Subscription API...")
    # Get plans
    resp = requests.get(f"{BASE_URL}/subscription/plans")
    print(f"Plans: {resp.status_code} - Found {len(resp.json())} plans")
    
    # Initializing payment
    resp = requests.post(f"{BASE_URL}/subscription/initialize", params={
        "plan_id": "growth",
        "email": "test@example.com"
    })
    print(f"Initialize: {resp.status_code}")
    if resp.status_code == 200:
        print(f"Auth URL: {resp.json().get('authorization_url')}")

if __name__ == "__main__":
    try:
        test_waitlist()
        test_subscriptions()
    except Exception as e:
        print(f"Verification failed: {e}")
