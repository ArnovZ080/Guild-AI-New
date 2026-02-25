from .connectors.hubspot import HubSpotIntegration
from .connectors.twitter import TwitterIntegration
from .connectors.google_calendar import GoogleCalendarIntegration
from .connectors.stripe import StripeIntegration
from .connectors.sendgrid import SendGridIntegration
from .base import IntegrationRegistry

def register_all_connectors():
    """Register all core connectors into the integration registry."""
    IntegrationRegistry.register("hubspot", HubSpotIntegration)
    IntegrationRegistry.register("twitter", TwitterIntegration)
    IntegrationRegistry.register("google_calendar", GoogleCalendarIntegration)
    IntegrationRegistry.register("stripe", StripeIntegration)
    IntegrationRegistry.register("sendgrid", SendGridIntegration)
    # Recruitment etc. can be added here
    print("All core connectors registered.")
