from typing import Any, Dict, Optional
import os
import logging
import asyncio
from services.core.agents.base import BaseAgent
from services.core.agents.registry import AgentRegistry, AgentCapability

# External libraries for Voice, wrapped in try-except
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import librosa
    import soundfile as sf
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

logger = logging.getLogger(__name__)

class VoiceAgent(BaseAgent):
    """
    Voice Agent implementing Audio Processing, TTS, and STT capabilities.
    Ported from legacy VoiceAgent.
    """
    
    def __init__(self, config: Any = None):
        super().__init__(config)
        self.tts_pipeline = None
        self.stt_pipeline = None
        if TRANSFORMERS_AVAILABLE:
            # Lazy load pipelines to avoid startup overhead
            pass

    async def process(self, input_data: Any, context: Optional[Dict] = None) -> Any:
        command = input_data.get("command", "synthesize_speech")
        
        if command == "synthesize_speech":
            return await self.synthesize_speech(input_data)
        elif command == "transcribe_audio":
            return await self.transcribe_audio(input_data)
        elif command == "process_audio":
            return await self.process_audio(input_data)
        else:
            return {"error": f"Unknown command: {command}"}

    async def synthesize_speech(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert text to speech."""
        text = input_data.get("text", "")
        if not text:
            return {"error": "No text provided"}
            
        if not TRANSFORMERS_AVAILABLE:
            return {"status": "failed", "message": "Transformers library not available"}

        try:
            if not self.tts_pipeline:
                self.tts_pipeline = pipeline("text-to-speech", model="microsoft/speecht5_tts")
            
            # Simple TTS generation using Transformers pipeline
            speech = self.tts_pipeline(text)
            
            # Use 'file_path' or return audio bytes/buffer
            output_path = input_data.get("output_path", "output.wav")
            
            if LIBROSA_AVAILABLE and isinstance(speech, dict) and 'audio' in speech:
                import soundfile as sf
                sf.write(output_path, speech['audio'], speech['sampling_rate'])
                return {"status": "success", "file_path": output_path}
            
            return {"status": "success", "message": "Speech generated (placeholder)"}
            
        except Exception as e:
            logger.error(f"TTS failed: {e}")
            return {"status": "error", "message": str(e)}

    async def transcribe_audio(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert speech to text."""
        audio_path = input_data.get("audio_path", "")
        if not os.path.exists(audio_path):
             return {"error": "Audio file not found"}

        if not TRANSFORMERS_AVAILABLE:
             return {"status": "failed", "message": "Transformers library not available"}

        try:
            if not self.stt_pipeline:
                 self.stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")
            
            result = self.stt_pipeline(audio_path)
            return {"status": "success", "transcription": result.get("text", "")}

        except Exception as e:
            logger.error(f"STT failed: {e}")
            return {"status": "error", "message": str(e)}

    async def process_audio(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance audio quality."""
        # implementation placeholder
        return {"status": "not_implemented", "message": "Audio processing not fully implemented"}


# Register Agent
AgentRegistry.register(AgentCapability(
    name="VoiceAgent",
    category="Interface",
    capabilities=["text_to_speech", "speech_to_text", "audio_processing"],
    description="Handles voice interactions, including TTS and STT.",
    agent_class=VoiceAgent
))
