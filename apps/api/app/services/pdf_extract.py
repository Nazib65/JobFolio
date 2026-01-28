"""
PDF text extraction and resume parsing service.
"""

import re 
import hashlib 
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, BinaryIO
import logging 

logger = logging.getLogger(__name__)

@dataclass
class ExtractedResume:
    """
    Result of PDF text extraction.
    """
    raw_text: str 
    lines: list[str]
    bullet_points: list[dict]
    page_count: int 
    file_hash: str 
    extraction_method: str = "pdfplumber"
    errors: list[str] = field(default_factory=list)

class PDFextractor:
    """
    Extract text from PDF resumes.
    Uses pdfplumber for extraction.
    """
    BULLET_POINTS = [
        re.compile(r'^[\s]*[•●○◦▪▸►‣⁃]\s*(.+)$'),
        re.compile(r'^[\s]*[-–—]\s*(.+)$'),
        re.compile(r'^[\s]*\*\s+(.+)$'),
        re.compile(r'^[\s]*\d+[.)]\s+(.+)$'),  
        re.compile(r'^[\s]*[a-z][.)]\s+(.+)$', re.I),
    ]

    # Section headers that provide context
    SECTION_PATTERNS ={
        'experience': re.compile(r'^(experience|work\s*history|employment|professional\s*experience)', re.I),
        'education': re.compile(r'^(education|academic|degrees?|certifications?)', re.I),
        'skills': re.compile(r'^(skills?|technical\s*skills?|core\s*competenc)', re.I),
        'projects': re.compile(r'^(projects?|portfolio|personal\s*projects?)', re.I),
        'leadership': re.compile(r'^(leadership|activities|extracurriculars?)', re.I),
        'summary': re.compile(r'^(summary|objective|profile|about)', re.I),
    }

    # Company/title pattern 
    COMPANY_TITLE_PATTERN = re.compile(
        r'^([A-Z][A-Za-z\s&.,]+(?:Inc|LLC|Corp|Ltd|Company)?)\s*[-–|]\s*(.+)$'
    )
    
    @classmethod
    async def extract_from_file(cls, file_path: Path) -> ExtractedResume:
        """
        Extract text from a PDF file.
        """
        import pdfplumber 

        errors=[]
        raw_text =""
        page_count=0

        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            with pdfplumber.open(file_path) as pdf:
                page_count = len(pdf.pages)
                pages_text = []

                for i, page in enumerate(pdf.pages):
                    try:
                        text = page.extract_text() or ""
                        pages_text.append(text)
                    except Exception as e:
                        errors.append(f"Page {i+1}: {str(e)}")
                        pages_text.append("")
                raw_text ='\n\n'.join(pages_text)
        except Exception as e:
            logger.error(f"Failed to extract PDF: {str(e)}")
            errors.append(f"Extraction failed: {str(e)}")
            return ExtractedResume(
                raw_text="",
                lines=[],
                bullet_points=[],
                page_count=0,
                file_hash="",
                errors=errors,
            )
        #Process extratcted text
        lines = cls._segment_lines(raw_text)
        bullet_points =cls._extract_bullet_points(lines)

        return ExtractedResume(
            raw_text = raw_text,
            lines = lines,
            bullet_points = bullet_points,
            page_count = page_count,
            file_hash = file_hash,
            errors = errors,
        )
    
    @classmethod
    async def extract_from_bytes(cls, file_content: bytes, filename:str = "resume.pdf")->ExtractedResume:
        """
        Extract text from PDF bytes.
        """
        import pdfplumber 
        from io import BytesIO

        errors=[]
        raw_text =""
        page_count=0

        file_hash = hashlib.sha256(file_content).hexdigest()

        try:
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                page_count = len(pdf.pages)
                pages_text = []

                for i, page in enumerate(pdf.pages):
                    try:
                        text = page.extract_text() or ""
                        pages_text.append(text)
                    except Exception as e:
                        errors.append(f"Page {i+1}: {str(e)}")
                        pages_text.append("")
                raw_text ='\n\n'.join(pages_text)
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            errors.append(f"Extraction failed: {str(e)}")
            return ExtractedResume(
                raw_text="",
                lines=[],
                bullet_points=[],
                page_count=0,
                file_hash=file_hash,
                errors=errors,
            )
        # Process extracted text
        lines = cls._segment_lines(raw_text)
        bullet_points =cls._extract_bullet_points(lines)
        return ExtractedResume(
            raw_text = raw_text,
            lines = lines,
            bullet_points = bullet_points,
            page_count = page_count,
            file_hash = file_hash,
            errors = errors,
        )
    @classmethod
    def _segmet_lines(cls, raw_text:str) -> list[str]:
        """
        Segment text into meaningful lines.
        """
        if not raw_text:
            return []
        
        # Split on newlines
        lines= raw_text.split('\n')

        # Clean each line 
        cleaned=[]
        for line in lines:
            line = line.strip()

            # skip empty lines
            if not line:
                continue

            # Skip every short lines 
            if len(line)< 3:
                continue

            # Skip page number 
            if re.match(r'^(Page\s*)?\d+(\s*of\s*\d+)?$', line, re.I):  
                continue
            cleaned.append(line)
        return cleaned 
    
    @classmethod
    def _extract_bullet_points(cls, lines:list[str]) -> list[dict]:
        """
        Extract bullet points with context.
        """
        bullet_points=[]
        current_context=None 
        current_section=None

        for i, line in enumerate(lines):
            # Check for section headers
            for section, pattern in cls.SECTION_PATTERNS.items():
                if pattern.match(line):
                    current_section = section
                    current_context = None  
                    break

                if current_section=='experience':
                    company_match=cls.COMPANY_TITLE_PATTERN.match(line)
                    if company_match:
                        current_context = f"{company_match.group(1).strip()} - {company_match.group(2).strip()}"
                        break
                
                for pattern in cls.BULLET_POINTS:
                    match = pattern.match(line)
                    if match:
                        bullet_text = match.group(1).strip() if match.groups() else line.strip()
                        
                        if len(bullet_text) < 5:
                            continue

                        bullet_points.append({
                            'text': bullet_text,
                            'line_number': i,
                            'context': current_context,
                            'section': current_section,
                        })
                        break
                else:
                    if (current_section == 'experience' and 
                    len(line) > 30 and 
                    not any(p.match(line) for p in cls.SECTION_PATTERNS.values())):
                        # Heuristic: Lines with action verbs at start are likely accomplishments
                        if re.match(r'^(Developed|Built|Created|Implemented|Managed|Led|Designed|'
                                r'Improved|Increased|Reduced|Achieved|Delivered|Launched|Established)',
                                line, re.I):
                            bullet_points.append({
                                "text": line,
                                "context": current_context,
                                "line_number": i,
                                "section": current_section,
                            })
            
        return bullet_points

class ResumeParser:
    """
    Parsed structured data from resume text.    
    """
    @classmethod
    def parse_basic_structure(cls, lines: list[str]) -> dict:
        """
        Parse basic structure: sections and headings.
        """
        sections ={
            'summary': [],
            'experience': [],
            'education': [],
            'skills': [],
            'projects': [],
            'leadership': [],
            'other': [],
        }
        current_section ='summary'

        for line in lines:
            for section, pattern in PDFextractor.SECTION_PATTERNS.items():
                if pattern.match(line):
                    current_section = section
                    break
            else:
                sections[current_section].append(line)
        
        contact_hints = cls._extract_contact_hints(lines[:10])
        skills_raw=cls._extract_skills_list(sections.get('skills', []))
        return{
            "sections": sections, 
            "contact_hints": contact_hints,
            "skills_raw": skills_raw,
        }
    @classmethod
    def _extract_contact_hints(cls, header_lines: list[str]) -> dict:
        """Extract potential contact information from header."""
        hints = {}
        
        for line in header_lines:
            # Email
            email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)
            if email_match:
                hints['email'] = email_match.group()
            
            # Phone
            phone_match = re.search(r'[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}', line)
            if phone_match:
                hints['phone'] = phone_match.group()
            
            # LinkedIn
            linkedin_match = re.search(r'linkedin\.com/in/([\w-]+)', line, re.I)
            if linkedin_match:
                hints['linkedin'] = linkedin_match.group(1)
            
            # GitHub
            github_match = re.search(r'github\.com/([\w-]+)', line, re.I)
            if github_match:
                hints['github'] = github_match.group(1)
        
        return hints
    
    @classmethod
    def _extract_skills_list(cls, skill_lines: list[str]) -> list[str]:
        """Extract individual skills from skills section."""
        skills = []
        
        for line in skill_lines:
            # Skills are often comma or pipe separated
            parts = re.split(r'[,|•●]\s*', line)
            for part in parts:
                skill = part.strip()
                if skill and len(skill) > 1 and len(skill) < 50:
                    skills.append(skill)
        
        return skills