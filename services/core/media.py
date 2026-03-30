"""
Guild-AI Media Generation
Images: Imagen 3 via Vertex AI
Video:  Veo 3 / Veo 3 Fast via Vertex AI
"""
import asyncio
import logging
from typing import Optional, List, Dict, Any
from enum import Enum

from services.core.config import settings

logger = logging.getLogger(__name__)


# ── Aspect Ratios ──

class ImageAspectRatio(Enum):
    SQUARE = "1:1"
    PORTRAIT = "9:16"
    LANDSCAPE = "16:9"
    POST = "4:5"


class VideoAspectRatio(Enum):
    LANDSCAPE = "16:9"
    PORTRAIT = "9:16"


# ── Image Generation (Imagen 3) ──

class ImageGenerator:
    """Generate images using Imagen 3 on Vertex AI."""

    async def generate(
        self,
        prompt: str,
        aspect_ratio: ImageAspectRatio = ImageAspectRatio.SQUARE,
        count: int = 1,
        negative_prompt: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate images from a text prompt.

        Returns list of dicts with `index`, `image_bytes`, `mime_type`.
        """
        from vertexai.preview.vision_models import ImageGenerationModel

        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

        kwargs: Dict[str, Any] = {
            "prompt": prompt,
            "number_of_images": min(count, 4),
            "aspect_ratio": aspect_ratio.value,
        }
        if negative_prompt:
            kwargs["negative_prompt"] = negative_prompt

        # Imagen is synchronous — run in executor
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: model.generate_images(**kwargs)
        )

        results = []
        for i, image in enumerate(response.images):
            results.append({
                "index": i,
                "image_bytes": image._image_bytes,
                "mime_type": "image/png",
            })

        logger.info("Generated %d image(s) for prompt: %.60s...", len(results), prompt)
        return results


# ── Video Generation (Veo 3) ──

class VideoGenerator:
    """Generate videos using Veo 3 / Veo 3 Fast on Vertex AI."""

    async def generate(
        self,
        prompt: str,
        aspect_ratio: VideoAspectRatio = VideoAspectRatio.PORTRAIT,
        duration_seconds: int = 8,
        negative_prompt: Optional[str] = None,
        use_fast: bool = True,
    ) -> Dict[str, Any]:
        """
        Initiate video generation from a text prompt.

        Veo 3 uses a long-running operation pattern. This method starts the
        generation and returns the operation handle. Poll `check_status()` for
        completion.

        Args:
            prompt: Text description of the video.
            aspect_ratio: Portrait (9:16) for reels, Landscape (16:9) for ads.
            duration_seconds: Target duration (Veo 3 supports up to ~8s per clip).
            negative_prompt: What to avoid in generation.
            use_fast: Use Veo 3 Fast (cheaper, faster) vs Veo 3 (higher quality).

        Returns:
            Dict with `status`, `model`, `prompt`, `aspect_ratio`, `operation_name`.
        """
        model_id = "veo-3.0-fast-generate" if use_fast else "veo-3.0-generate"

        try:
            from google.cloud import aiplatform_v1beta1 as aiplatform

            client = aiplatform.PredictionServiceClient(
                client_options={
                    "api_endpoint": f"{settings.GCP_LOCATION}-aiplatform.googleapis.com"
                }
            )

            endpoint = (
                f"projects/{settings.GCP_PROJECT_ID}/locations/{settings.GCP_LOCATION}"
                f"/publishers/google/models/{model_id}"
            )

            instance = {"prompt": prompt}
            parameters: Dict[str, Any] = {
                "aspectRatio": aspect_ratio.value,
                "sampleCount": 1,
                "durationSeconds": duration_seconds,
            }
            if negative_prompt:
                parameters["negativePrompt"] = negative_prompt

            loop = asyncio.get_event_loop()
            operation = await loop.run_in_executor(
                None,
                lambda: client.predict(
                    endpoint=endpoint,
                    instances=[instance],
                    parameters=parameters,
                ),
            )

            logger.info("Video generation initiated. Model: %s", model_id)

            return {
                "status": "generating",
                "model": model_id,
                "prompt": prompt,
                "aspect_ratio": aspect_ratio.value,
                "operation_name": str(operation),
            }

        except Exception as e:
            logger.error("Video generation failed: %s", e)
            return {
                "status": "error",
                "model": model_id,
                "prompt": prompt,
                "error": str(e),
            }


# ── Global instances ──
image_generator = ImageGenerator()
video_generator = VideoGenerator()
