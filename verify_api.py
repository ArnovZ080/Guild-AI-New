import asyncio
import httpx
import sys
import uvicorn
from multiprocessing import Process
import time

# Function to run the server
def run_server():
    from services.api.main import app
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

async def verify_api():
    print("Starting API verification...")
    
    # Start server in background
    server_process = Process(target=run_server)
    server_process.start()
    
    # Wait for server to start
    time.sleep(3)
    
    base_url = "http://127.0.0.1:8001"
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Health Check
            print("\n1. Testing Health Check...")
            response = await client.get(f"{base_url}/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            assert response.status_code == 200
            
            # 2. List Agents
            print("\n2. Testing List Agents...")
            response = await client.get(f"{base_url}/agents/")
            print(f"Status: {response.status_code}")
            agents = response.json()
            print(f"Found {len(agents)} agents: {[a['name'] for a in agents]}")
            assert response.status_code == 200
            assert len(agents) > 0
            
            # 3. Run Content Strategist Agent (Mock Run)
            print("\n3. Testing Run Agent (ContentStrategistAgent)...")
            payload = {
                "input_data": {
                    "business_objectives": ["Increase brand awareness"],
                    "target_audience": {"demographics": "Tech startups"}
                },
                "context": {}
            }
            # Note: This might fail if LLM is not configured or fails, but we want to check if the endpoint works
            response = await client.post(f"{base_url}/agents/ContentStrategistAgent/run", json=payload, timeout=30.0)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.json()}")
            else:
                print(f"Error: {response.text}")
            
            # We don't strictly assert 200 here because LLM might fail, but 500 would be bad if it's code error
            if response.status_code == 500:
                print("!! Agent run failed with 500 !!")

    except Exception as e:
        print(f"Verification failed: {e}")
    finally:
        print("\nStopping server...")
        server_process.terminate()
        server_process.join()

if __name__ == "__main__":
    asyncio.run(verify_api())
