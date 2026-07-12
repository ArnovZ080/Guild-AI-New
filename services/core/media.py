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
    """Generate images using Gemini 2.5 Flash Image on Vertex AI."""

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
        from google import genai
        from google.genai import types

        client = genai.Client(vertexai=True, project=settings.GCP_PROJECT_ID, location=settings.GCP_LOCATION)

        config = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        )
        
        # Imagen is synchronous — run in executor
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: client.models.generate_content(
                model=settings.IMAGE_MODEL,
                contents=prompt,
                config=config,
            )
        )

        results = []
        if hasattr(response, 'candidates') and response.candidates:
            for i, part in enumerate(response.candidates[0].content.parts):
                if hasattr(part, 'inline_data') and part.inline_data:
                    results.append({
                        "index": i,
                        "image_bytes": part.inline_data.data,
                        "mime_type": "image/png",
                    })

        logger.info("Generated %d image(s) for prompt: %.60s...", len(results), prompt)
        return results


# ── Video Generation (Veo 3.1) ──

class VideoGenerator:
    """Generate videos using Veo 3.1 on Vertex AI."""

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

        WARNING: Blocking call, takes minutes — invoke only from Celery tasks or BackgroundTasks, never directly in a route handler.

        Args:
            prompt: Text description of the video.
            aspect_ratio: Portrait (9:16) for reels, Landscape (16:9) for ads.
            duration_seconds: Target duration.
            negative_prompt: What to avoid in generation.
            use_fast: Use Veo 3.1 Fast (cheaper, faster) vs Veo 3.1 (higher quality).

        Returns:
            Dict with `video_bytes`, `mime_type`, `model`.
        """
        import time
        from google import genai
        from google.genai import types
        from google.cloud import storage

        model_id = settings.VIDEO_MODEL_FAST if use_fast else settings.VIDEO_MODEL

        try:
            client = genai.Client(vertexai=True, project=settings.GCP_PROJECT_ID, location=settings.GCP_LOCATION)
            
            # GCS Bucket for Veo output
            output_gcs_uri = f"gs://guild-ai-080-media/veo/{int(time.time())}/"

            config = types.GenerateVideosConfig(
                number_of_videos=1,
                output_gcs_uri=output_gcs_uri,
                aspect_ratio=aspect_ratio.value,
            )
            
            loop = asyncio.get_event_loop()
            
            logger.info("Initiating video generation on model: %s. Output: %s", model_id, output_gcs_uri)
            operation = await loop.run_in_executor(
                None,
                lambda: client.models.generate_videos(
                    model=model_id,
                    prompt=prompt,
                    config=config
                )
            )

            # Polling loop
            start_time = time.time()
            max_wait = 6 * 60  # 6 minutes timeout

            while not operation.done:
                if time.time() - start_time > max_wait:
                    raise TimeoutError(f"Video generation timed out after {max_wait} seconds.")
                await asyncio.sleep(15)
                operation = await loop.run_in_executor(
                    None,
                    lambda: client.operations.get(operation=operation.name)
                )

            if operation.error:
                raise Exception(f"Video generation error: {operation.error}")

            result = operation.response or operation.result
            if not result or not hasattr(result, 'generated_videos') or not result.generated_videos:
                raise Exception("No videos returned in operation response")

            video_uri = result.generated_videos[0].uri
            
            # Download from GCS
            bucket_name = video_uri.replace("gs://", "").split("/")[0]
            blob_path = "/".join(video_uri.replace("gs://", "").split("/")[1:])
            
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_path)
            video_bytes = blob.download_as_bytes()
            
            logger.info("Video generation completed successfully: %s", video_uri)

            return {
                "video_bytes": video_bytes,
                "mime_type": "video/mp4",
                "model": model_id,
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
