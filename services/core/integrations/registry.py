"""
Integration Registry.
Registers all core connectors so they are available via IntegrationRegistry.
"""
from .connectors.hubspot import HubSpotIntegration
from .connectors.twitter import TwitterIntegration
from .connectors.google_calendar import GoogleCalendarIntegration
from .connectors.stripe import StripeIntegration
from .connectors.sendgrid import SendGridIntegration
from .connectors.crm import (
    SalesforceIntegration, AsanaIntegration, TrelloIntegration,
    MondayIntegration, JiraIntegration
)
from .connectors.commerce import (
    PayPalIntegration, SquareIntegration, ShopifyIntegration,
    WooCommerceIntegration, AmazonIntegration
)
from .connectors.marketing import (
    MetaAdsIntegration, GoogleAdsIntegration as ConnectorGoogleAds,
    LinkedInAdsIntegration, MailchimpIntegration,
    ConvertKitIntegration, ActiveCampaignIntegration
)
from .connectors.social import (
    MetaSocialIntegration, LinkedInSocialIntegration, TikTokIntegration,
    IndeedIntegration, UpworkIntegration
)
from .connectors.extended import (
    GoogleAnalyticsIntegration, PipedriveIntegration,
    OutlookCalendarIntegration, FacebookPublishingIntegration
)
from .base import IntegrationRegistry


def register_all_connectors():
    """Register all core connectors into the integration registry."""
    # Standalone connectors
    IntegrationRegistry.register("hubspot", HubSpotIntegration)
    IntegrationRegistry.register("twitter", TwitterIntegration)
    IntegrationRegistry.register("google_calendar", GoogleCalendarIntegration)
    IntegrationRegistry.register("stripe", StripeIntegration)
    IntegrationRegistry.register("sendgrid", SendGridIntegration)

    # CRM
    IntegrationRegistry.register("salesforce", SalesforceIntegration)
    IntegrationRegistry.register("asana", AsanaIntegration)
    IntegrationRegistry.register("trello", TrelloIntegration)
    IntegrationRegistry.register("monday", MondayIntegration)
    IntegrationRegistry.register("jira", JiraIntegration)

    # Commerce
    IntegrationRegistry.register("paypal", PayPalIntegration)
    IntegrationRegistry.register("square", SquareIntegration)
    IntegrationRegistry.register("shopify", ShopifyIntegration)
    IntegrationRegistry.register("woocommerce", WooCommerceIntegration)
    IntegrationRegistry.register("amazon", AmazonIntegration)

    # Marketing
    IntegrationRegistry.register("meta_ads", MetaAdsIntegration)
    IntegrationRegistry.register("connector_google_ads", ConnectorGoogleAds)
    IntegrationRegistry.register("linkedin_ads", LinkedInAdsIntegration)
    IntegrationRegistry.register("mailchimp", MailchimpIntegration)
    IntegrationRegistry.register("convertkit", ConvertKitIntegration)
    IntegrationRegistry.register("activecampaign", ActiveCampaignIntegration)

    # Social & Job Boards
    IntegrationRegistry.register("meta_social", MetaSocialIntegration)
    IntegrationRegistry.register("linkedin_social", LinkedInSocialIntegration)
    IntegrationRegistry.register("tiktok", TikTokIntegration)
    IntegrationRegistry.register("indeed", IndeedIntegration)
    IntegrationRegistry.register("upwork", UpworkIntegration)

    # Extended (Phase 2)
    IntegrationRegistry.register("google_analytics", GoogleAnalyticsIntegration)
    IntegrationRegistry.register("pipedrive", PipedriveIntegration)
    IntegrationRegistry.register("outlook_calendar", OutlookCalendarIntegration)
    IntegrationRegistry.register("facebook", FacebookPublishingIntegration)

    print(f"All {len(IntegrationRegistry.list_integrations())} connectors registered.")
