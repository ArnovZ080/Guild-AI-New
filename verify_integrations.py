import asyncio
import sys
import os
from unittest.mock import AsyncMock, patch

sys.path.append(os.getcwd())

from services.core.integrations.base import IntegrationConfig, IntegrationRegistry
# Import to register
import services.core.integrations.social 

async def main():
    print("Verifying Integrations...")
    
    # 1. Test Registry Discovery
    available = IntegrationRegistry.list_integrations()
    print(f"Available Integrations: {available}")
    
    if "twitter" not in available or "linkedin" not in available:
        print("FAILED: Social integrations not registered.")
        return

    # 2. Test Twitter Initialization & Mock Posting
    print("\nTesting Twitter Integration...")
    twitter_config = IntegrationConfig(
        name="my_twitter",
        credentials={"access_token": "fake_token", "user_id": "123"}
    )
    
    twitter_integration = IntegrationRegistry.initialize_integration("twitter", twitter_config)
    
    # Mock the net request
    with patch.object(twitter_integration, '_make_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"id": "tweet_123", "text": "Hello World"}
        
        result = await twitter_integration.post_content("Hello World")
        print(f"Twitter Post Result: {result}")
        
        mock_request.assert_called_once()
        print("Twitter: SUCCESS")

    # 3. Test LinkedIn Initialization
    print("\nTesting LinkedIn Integration...")
    linkedin_config = IntegrationConfig(
        name="my_linkedin",
        credentials={"access_token": "fake_token"}
    )
    linkedin_integration = IntegrationRegistry.initialize_integration("linkedin", linkedin_config)
    
    # Mock get_profile AND post
    with patch.object(linkedin_integration, '_make_request', new_callable=AsyncMock) as mock_li_req:
        # First call: get_profile, Second call: post_content
        mock_li_req.side_effect = [
            {"id": "user_456"}, # get_profile response
            {"id": "post_789"}  # post response
        ]
        
        result = await linkedin_integration.post_content("Hello LinkedIn")
        print(f"LinkedIn Post Result: {result}")
        
        assert mock_li_req.call_count == 2
        print("LinkedIn: SUCCESS")

    # 4. Test Google Integration
    print("\nTesting Google Integration...")
    google_config = IntegrationConfig(
        name="my_google",
        credentials={"token": "fake_token"}
    )
    google_int = IntegrationRegistry.initialize_integration("google", google_config)
    
    files = await google_int.list_files()
    print(f"Google Files: {files}")
    assert len(files) > 0
    
    doc = await google_int.create_doc("Test Doc", "Hello World")
    print(f"Created Doc: {doc}")
    assert doc["title"] == "Test Doc"
    print("Google: SUCCESS")

    # 5. Test Ads Integration
    print("\nTesting Google Ads Integration...")
    ads_config = IntegrationConfig(
        name="my_google_ads",
        credentials={"access_token": "fake", "customer_id": "123"}
    )
    ads_int = IntegrationRegistry.initialize_integration("google_ads", ads_config)
    # We don't mock the _make_request here because create_campaign is currently mocked inside the class
    # In a full impl we would mock _make_request.
    
    campaign = await ads_int.create_campaign("Summer Sale", 1000.0, "TRAFFIC")
    print(f"Created Campaign: {campaign}")
    assert campaign.id == "ga_camp_123"
    print("Google Ads: SUCCESS")

    # 6. Test CRM Integrations
    print("\nTesting CRM Integrations...")
    
    # HubSpot
    hs_config = IntegrationConfig(name="my_hubspot", credentials={"access_token": "fake"})
    hs_int = IntegrationRegistry.initialize_integration("hubspot", hs_config)
    hs_contact = await hs_int.create_contact("test@hubspot.com", "Hub", "Spot")
    print(f"Created HubSpot Contact: {hs_contact}")
    assert hs_contact.email == "test@hubspot.com"
    print("HubSpot: SUCCESS")

    # Salesforce
    sf_config = IntegrationConfig(name="my_salesforce", credentials={"access_token": "fake", "instance_url": "https://na1.salesforce.com"})
    sf_int = IntegrationRegistry.initialize_integration("salesforce", sf_config)
    sf_contacts = await sf_int.get_contacts()
    print(f"Fetcher Salesforce Contacts: {len(sf_contacts)}")
    assert len(sf_contacts) > 0
    print("Salesforce: SUCCESS")

    # 7. Test SEO Integrations
    print("\nTesting SEO Integrations...")
    
    # Ahrefs
    ahrefs_config = IntegrationConfig(name="my_ahrefs", credentials={"api_key": "fake"})
    ahrefs_int = IntegrationRegistry.initialize_integration("ahrefs", ahrefs_config)
    kw_data = await ahrefs_int.get_keyword_data("ai agents")
    print(f"Ahrefs Keyword: {kw_data}")
    assert kw_data.keyword == "ai agents"
    print("Ahrefs: SUCCESS")

    # SEMrush
    sem_config = IntegrationConfig(name="my_semrush", credentials={"api_key": "fake"})
    sem_int = IntegrationRegistry.initialize_integration("semrush", sem_config)
    kw_data_sem = await sem_int.get_keyword_overview("seo tools")
    print(f"SEMrush Keyword: {kw_data_sem}")
    assert kw_data_sem.keyword == "seo tools"
    print("SEMrush: SUCCESS")

    print("\nAll Integration Tests Passed!")

if __name__ == "__main__":
    asyncio.run(main())
