from fastapi.testclient import TestClient
from services.mcp.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("Health Check: SUCCESS")

def test_create_campaign():
    payload = {
        "platform": "google_ads",
        "name": "MCP Verification Campaign",
        "budget": 500.0,
        "objective": "TRAFFIC"
    }
    response = client.post("/mcp/tools/create_campaign", json=payload)
    if response.status_code != 200:
        print(f"Create Campaign Failed: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["campaign"]["name"] == "MCP Verification Campaign"
    print("Create Campaign (Google Ads): SUCCESS")

def test_crm_contacts():
    # Create Contact
    payload = {
        "platform": "hubspot",
        "email": "mcp@test.com",
        "first_name": "MCP",
        "last_name": "Tester"
    }
    response = client.post("/mcp/tools/create_contact", json=payload)
    assert response.status_code == 200
    assert response.json()["contact"]["email"] == "mcp@test.com"
    print("Create Contact (HubSpot): SUCCESS")

    # Get Contacts
    payload_get = {"platform": "hubspot"}
    response_get = client.post("/mcp/tools/get_contacts", json=payload_get)
    assert response_get.status_code == 200
    assert len(response_get.json()["contacts"]) > 0
    print("Get Contacts (HubSpot): SUCCESS")

def test_seo_research():
    payload = {
        "platform": "ahrefs",
        "keyword": "autonomous agents"
    }
    response = client.post("/mcp/tools/keyword_research", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["keyword"] == "autonomous agents"
    # assert data["data"]["search_volume"] == 1500 # Mock value
    print("SEO Research (Ahrefs): SUCCESS")

if __name__ == "__main__":
    print("Verifying MCP Service...")
    test_health()
    test_create_campaign()
    test_crm_contacts()
    test_seo_research()
    print("\nAll MCP Tests Passed!")
