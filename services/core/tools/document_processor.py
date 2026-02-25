import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import tempfile

# Conditional import for MarkItDown
try:
    from markitdown import MarkItDown
    MARKITDOWN_AVAILABLE = True
except ImportError:
    MARKITDOWN_AVAILABLE = False

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Document Processor using MarkItDown to convert various formats to Markdown.
    Ported from legacy MarkItDownProcessor.
    """
    
    def __init__(self):
        self.supported_extensions = {
            '.pdf', '.docx', '.pptx', '.xlsx', '.doc', '.ppt', '.xls',
            '.txt', '.html', '.htm', '.md', '.rtf', '.odt', '.odp', '.ods',
            '.mp3', '.mp4', '.wav' 
        }
        self.md_converter = None
        if MARKITDOWN_AVAILABLE:
            try:
                self.md_converter = MarkItDown()
            except Exception as e:
                logger.warning(f"Failed to initialize MarkItDown: {e}")

    def is_supported(self, file_path: str) -> bool:
        return Path(file_path).suffix.lower() in self.supported_extensions

    def convert_to_markdown(self, file_path: str) -> Optional[str]:
        """Convert a document to Markdown."""
        if not MARKITDOWN_AVAILABLE or not self.md_converter:
            logger.error("MarkItDown is not available.")
            return None
            
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None

            result = self.md_converter.convert(file_path)
            
            if result and result.text_content:
                return result.text_content.strip()
            return None
            
        except Exception as e:
            logger.error(f"Error converting {file_path}: {e}")
            return None

    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process a document and return structure suitable for indexing."""
        markdown_content = self.convert_to_markdown(file_path)
        
        if not markdown_content:
            return {"status": "failed", "error": "Conversion failed or empty content"}
            
        return {
            "status": "success",
            "content": markdown_content,
            "metadata": {
                "source": file_path,
                "format": Path(file_path).suffix.lower(),
                "length": len(markdown_content)
            }
        }

# Global instance
document_processor = DocumentProcessor()
