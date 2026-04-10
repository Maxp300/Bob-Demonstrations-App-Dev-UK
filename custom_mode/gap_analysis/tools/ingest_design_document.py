"""
Ingest Design Document Tool
Process design artifacts and extract requirements
"""

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import PyPDF2


@dataclass
class DesignDocument:
    """Represents a processed design document"""
    file_path: str
    document_type: str
    content: str
    metadata: Dict[str, Any]
    requirements: List[Dict[str, Any]]
    success: bool
    error: Optional[str] = None


class IngestDesignDocumentTool:
    """Tool for ingesting and processing design documents"""
    
    def __init__(self):
        self.name = "ingest_design_document"
        self.description = "Process design artifacts and extract requirements"
        
    def execute(
        self,
        file_path: str,
        document_type: Optional[str] = None,
        extraction_method: str = "pypdf2",
        output_format: str = "structured"
    ) -> DesignDocument:
        """
        Execute the tool to ingest a design document
        
        Args:
            file_path: Path to the design document
            document_type: Type of document (pdf, docx, markdown, image)
            extraction_method: Method to use (pypdf2, docling, ocr)
            output_format: Format for extracted content (text, structured)
            
        Returns:
            DesignDocument object with extracted content and metadata
        """
        try:
            # Auto-detect document type if not provided
            if not document_type:
                document_type = self._detect_document_type(file_path)
            
            # Extract content based on document type
            if document_type == "pdf":
                return self._process_pdf(file_path, extraction_method, output_format)
            elif document_type == "markdown":
                return self._process_markdown(file_path, output_format)
            elif document_type == "docx":
                return self._process_docx(file_path, output_format)
            else:
                return DesignDocument(
                    file_path=file_path,
                    document_type=document_type,
                    content="",
                    metadata={},
                    requirements=[],
                    success=False,
                    error=f"Unsupported document type: {document_type}"
                )
                
        except Exception as e:
            return DesignDocument(
                file_path=file_path,
                document_type=document_type or "unknown",
                content="",
                metadata={},
                requirements=[],
                success=False,
                error=str(e)
            )
    
    def _detect_document_type(self, file_path: str) -> str:
        """Detect document type from file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        type_map = {
            '.pdf': 'pdf',
            '.md': 'markdown',
            '.markdown': 'markdown',
            '.docx': 'docx',
            '.doc': 'doc',
            '.txt': 'text',
            '.png': 'image',
            '.jpg': 'image',
            '.jpeg': 'image'
        }
        return type_map.get(ext, 'unknown')
    
    def _process_pdf(
        self,
        file_path: str,
        extraction_method: str,
        output_format: str
    ) -> DesignDocument:
        """Process PDF document"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract metadata
                metadata = {
                    'num_pages': len(pdf_reader.pages),
                    'title': pdf_reader.metadata.title if pdf_reader.metadata else None,
                    'author': pdf_reader.metadata.author if pdf_reader.metadata else None,
                    'extraction_method': extraction_method
                }
                
                # Extract text from all pages
                content_parts = []
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text.strip():
                        content_parts.append(f"[Page {page_num}]\n{text}\n")
                
                content = "\n".join(content_parts)
                
                # Extract requirements (basic keyword-based extraction)
                requirements = self._extract_requirements(content)
                
                return DesignDocument(
                    file_path=file_path,
                    document_type='pdf',
                    content=content,
                    metadata=metadata,
                    requirements=requirements,
                    success=True
                )
                
        except Exception as e:
            return DesignDocument(
                file_path=file_path,
                document_type='pdf',
                content="",
                metadata={},
                requirements=[],
                success=False,
                error=f"PDF processing error: {str(e)}"
            )
    
    def _process_markdown(self, file_path: str, output_format: str) -> DesignDocument:
        """Process Markdown document"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            metadata = {
                'file_size': os.path.getsize(file_path),
                'line_count': len(content.split('\n'))
            }
            
            requirements = self._extract_requirements(content)
            
            return DesignDocument(
                file_path=file_path,
                document_type='markdown',
                content=content,
                metadata=metadata,
                requirements=requirements,
                success=True
            )
            
        except Exception as e:
            return DesignDocument(
                file_path=file_path,
                document_type='markdown',
                content="",
                metadata={},
                requirements=[],
                success=False,
                error=f"Markdown processing error: {str(e)}"
            )
    
    def _process_docx(self, file_path: str, output_format: str) -> DesignDocument:
        """Process DOCX document (placeholder - requires python-docx)"""
        return DesignDocument(
            file_path=file_path,
            document_type='docx',
            content="",
            metadata={},
            requirements=[],
            success=False,
            error="DOCX processing not yet implemented. Install python-docx library."
        )
    
    def _extract_requirements(self, content: str) -> List[Dict[str, Any]]:
        """Extract requirements from content using keyword matching"""
        requirements = []
        requirement_keywords = [
            'must', 'shall', 'should', 'required', 'requirement',
            'specification', 'design', 'architecture', 'implement'
        ]
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in requirement_keywords):
                if len(line.strip()) > 20:  # Filter out short lines
                    requirements.append({
                        'line_number': line_num,
                        'text': line.strip(),
                        'type': 'extracted',
                        'confidence': 0.7
                    })
        
        return requirements[:50]  # Limit to first 50 requirements


# Tool metadata for registration
TOOL_METADATA = {
    'name': 'ingest_design_document',
    'description': 'Process design artifacts and extract requirements',
    'parameters': {
        'file_path': {
            'type': 'string',
            'required': True,
            'description': 'Path to the design document'
        },
        'document_type': {
            'type': 'string',
            'required': False,
            'description': 'Type of document (pdf, docx, markdown, image)',
            'enum': ['pdf', 'docx', 'markdown', 'image', 'text']
        },
        'extraction_method': {
            'type': 'string',
            'required': False,
            'default': 'pypdf2',
            'description': 'Method to use for extraction',
            'enum': ['pypdf2', 'docling', 'ocr']
        },
        'output_format': {
            'type': 'string',
            'required': False,
            'default': 'structured',
            'description': 'Format for extracted content',
            'enum': ['text', 'structured']
        }
    },
    'returns': {
        'type': 'DesignDocument',
        'description': 'Processed design document with extracted content and requirements'
    }
}

# Made with Bob
