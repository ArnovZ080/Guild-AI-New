"""
Website Style Extractor

Scans a user's website, extracts CSS data, takes a screenshot,
and generates a comprehensive style.md using Gemini Multimodal.
"""
import logging
import socket
import ipaddress
import asyncio
from datetime import datetime
from urllib.parse import urlparse

from playwright.async_api import async_playwright
import vertexai
from vertexai.generative_models import GenerativeModel, Part

from services.core.config import settings

logger = logging.getLogger(__name__)

DEFAULT_STYLE = """# Brand Style Guide
## Generated from: Default (no website scanned or scan failed)

### Colour Palette
- Primary: #2563EB
- Secondary: #10B981
- Background: #FFFFFF
- Text Primary: #1F2937

### Typography
- Headings: sans-serif
- Body: sans-serif

### Overall Aesthetic
- Clean, standard fallback style
"""

def is_safe_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        
        # SSRF Guard
        ip = socket.gethostbyname(parsed.hostname)
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
            return False
    except Exception:
        return False
    return True

class WebsiteStyleExtractor:
    def __init__(self):
        try:
            vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_LOCATION)
            self.model = GenerativeModel(settings.GEMINI_FLASH_MODEL)
        except Exception as e:
            logger.error("Failed to initialize Vertex AI for Style Extractor: %s", e)
            self.model = None

    async def extract_style(self, url: str) -> str:
        """Extract style from website. Returns markdown string."""
        if not url or not is_safe_url(url):
            logger.warning(f"Unsafe or invalid URL: {url}")
            return DEFAULT_STYLE

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                try:
                    await page.goto(url, timeout=20000, wait_until="networkidle")
                    
                    # Programmatic extraction of CSS stats
                    css_data = await page.evaluate("""() => {
                        const counts = { bg: {}, color: {}, font: {} };
                        document.querySelectorAll('body, div, section, p, h1, h2, h3, h4, span, a, button').forEach(el => {
                            const style = window.getComputedStyle(el);
                            const bg = style.backgroundColor;
                            if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
                                counts.bg[bg] = (counts.bg[bg] || 0) + 1;
                            }
                            const c = style.color;
                            if (c) counts.color[c] = (counts.color[c] || 0) + 1;
                            
                            const f = style.fontFamily;
                            if (f) counts.font[f] = (counts.font[f] || 0) + 1;
                        });
                        
                        const getTop = (obj) => Object.entries(obj).sort((a,b) => b[1] - a[1]).slice(0, 5).map(x => x[0]);
                        return {
                            colors: getTop(counts.bg).concat(getTop(counts.color)),
                            fonts: getTop(counts.font)
                        };
                    }""")
                    
                    screenshot_bytes = await page.screenshot(full_page=True, type="png")
                finally:
                    await browser.close()
            
            if not self.model:
                return DEFAULT_STYLE
            
            # Send to Gemini Multimodal
            image_part = Part.from_data(screenshot_bytes, mime_type="image/png")
            prompt = f"""Analyze this website's visual design. Describe the aesthetic, colour mood, typography feel, and overall brand impression.
Here is some programmatically extracted CSS data to help ground your response:
Colors: {css_data.get('colors')}
Fonts: {css_data.get('fonts')}

Respond ONLY with a valid Markdown document matching this exact format:

# Brand Style Guide
## Generated from: {url}

### Colour Palette
(List the primary, secondary, background, and text colors using exact hex codes based on the provided CSS data and visual analysis)

### Typography
(Describe the fonts used for headings and body)

### Button Styles
(Describe the style of primary buttons)

### Spacing & Layout
(Describe layout patterns like border-radius, shadows, max-width)

### Imagery Style
(Describe photography, illustrations, icons)

### Overall Aesthetic
(Clean, modern, warm, professional, etc)
"""
            response = await self.model.generate_content_async([image_part, prompt])
            return response.text.strip().strip("```markdown").strip("```").strip()

        except Exception as e:
            logger.error(f"Error extracting style from {url}: {e}")
            return DEFAULT_STYLE

style_extractor = WebsiteStyleExtractor()
