import json
import os
from typing import Optional
from services.core.agents.models import BusinessIdentity
from services.core.logging import logger

class BusinessIdentityManager:
    """
    Manages the persistent profile of the user's business.
    """
    _instance: Optional[BusinessIdentity] = None
    _storage_path = "/Users/arnovanzyl/.gemini/antigravity/scratch/data/business_identity.json"

    @classmethod
    def get_identity(cls) -> BusinessIdentity:
        if cls._instance is None:
            cls.load()
        return cls._instance

    @classmethod
    def save(cls, identity: BusinessIdentity):
        cls._instance = identity
        os.makedirs(os.path.dirname(cls._storage_path), exist_ok=True)
        with open(cls._storage_path, 'w') as f:
            f.write(identity.json())
        logger.info(f"Business Identity saved for: {identity.business_name}")

    @classmethod
    def load(cls):
        if os.path.exists(cls._storage_path):
            with open(cls._storage_path, 'r') as f:
                data = json.load(f)
                cls._instance = BusinessIdentity(**data)
        else:
            # Phase 4 Default Expansion
            cls._instance = BusinessIdentity(
                business_name="The Artisanal Bakery",
                niche="High-end sourdough and French pastries",
                core_objectives=["Increase online orders by 40% in Q1", "Standardize brand voice across IG and YouTube"],
                brand={
                    "voice": "Warm, authentic, artisanal",
                    "tone": "Sophisticated but approachable",
                    "vocabulary": ["long-fermentation", "heritage grains", "crunch factor", "crumb"],
                    "dos": ["Focus on the process", "Highlight ingredients quality"],
                    "donts": ["Use overly corporate terms", "Promote ultra-processed additives"]
                },
                icp={
                    "ideal_client_description": "Health-conscious foodies who value tradition and quality over convenience.",
                    "demographics": {"age": "25-55", "location": "Urban areas"},
                    "psychographics": ["Values transparency", "Appreciates craftsmanship"],
                    "pain_points": ["Lack of high-quality local options", "Generic supermarket bread"],
                    "buying_triggers": ["Limited drops", "Seasonal specials"]
                },
                knowledge_base=[]
            )
            cls.save(cls._instance)

    @classmethod
    def get_context_prompt(cls) -> str:
        ident = cls.get_identity()
        return f"""
BUSINESS CONTEXT:
Name: {ident.business_name}
Niche: {ident.niche}

BRAND VOICE:
Voice: {ident.brand.voice}
Tone: {ident.brand.tone}
Vocabulary: {', '.join(ident.brand.vocabulary)}
Do's: {'; '.join(ident.brand.dos)}
Don'ts: {'; '.join(ident.brand.donts)}

IDEAL CLIENT PROFILE (ICP):
Target: {ident.icp.ideal_client_description}
Psychographics: {', '.join(ident.icp.psychographics)}
Pain Points: {', '.join(ident.icp.pain_points)}
"""

# Global manager access
identity_manager = BusinessIdentityManager()
