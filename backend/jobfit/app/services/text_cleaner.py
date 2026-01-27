"""
Text cleaning and metadata extraction service for job descriptions.
"""
import re
from dataclasses import dataclass
from typing import Optional
from html import unescape


@dataclass
class JobMetadata:
    """Extracted metadata from job description."""
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    seniority: Optional[str] = None
    role_type: Optional[str] = None
    remote_type: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None


@dataclass
class ExtractedSections:
    """Extracted sections from job description."""
    requirements: Optional[str] = None
    nice_to_have: Optional[str] = None
    responsibilities: Optional[str] = None
    benefits: Optional[str] = None


class TextCleaner:
    """Cleans and normalizes text from various sources."""
    
    # HTML tag pattern
    HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
    
    # Multiple whitespace
    MULTI_SPACE_PATTERN = re.compile(r'[ \t]+')
    MULTI_NEWLINE_PATTERN = re.compile(r'\n{3,}')
    
    # De-boilerplate patterns - common job board UI junk to remove
    BOILERPLATE_PATTERNS = [
        # Apply buttons and CTAs
        re.compile(r'^[\s]*apply\s*(now|today|here|for\s*this\s*job)?[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*click\s*(here\s*)?to\s*apply[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*submit\s*(your\s*)?(application|resume)[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*easy\s*apply[\s]*$', re.I | re.MULTILINE),
        # Job IDs and reference numbers
        re.compile(r'^[\s]*job\s*(id|number|#|ref|reference)[\s:]*[\w\-]+[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*requisition\s*(id|number|#)?[\s:]*[\w\-]+[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*posting\s*(id|number|#)?[\s:]*[\w\-]+[\s]*$', re.I | re.MULTILINE),
        # Share buttons
        re.compile(r'^[\s]*share\s*(this\s*)?(job|position)?[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*(share\s*on\s*)?(facebook|twitter|linkedin|email)[\s]*$', re.I | re.MULTILINE),
        # Save/bookmark
        re.compile(r'^[\s]*save\s*(this\s*)?(job|position)?[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*bookmark[\s]*$', re.I | re.MULTILINE),
        # Report/flag
        re.compile(r'^[\s]*report\s*(this\s*)?(job|listing)?[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*flag\s*as\s*inappropriate[\s]*$', re.I | re.MULTILINE),
        # Similar jobs
        re.compile(r'^[\s]*similar\s*jobs[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*related\s*(jobs|positions)[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*you\s*may\s*also\s*like[\s]*$', re.I | re.MULTILINE),
        # Navigation
        re.compile(r'^[\s]*back\s*to\s*(search|results|jobs)[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*(previous|next)\s*(job|page)?[\s]*$', re.I | re.MULTILINE),
        # Posted date standalone
        re.compile(r'^[\s]*posted\s*\d+\s*(days?|hours?|weeks?)\s*ago[\s]*$', re.I | re.MULTILINE),
        # View counts
        re.compile(r'^[\s]*\d+\s*(views?|applicants?)[\s]*$', re.I | re.MULTILINE),
        # Login prompts
        re.compile(r'^[\s]*(sign\s*in|log\s*in)\s*to\s*apply[\s]*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*create\s*(an\s*)?account[\s]*$', re.I | re.MULTILINE),
        # Cookie notices
        re.compile(r'^[\s]*we\s*use\s*cookies[\s]*.*$', re.I | re.MULTILINE),
        re.compile(r'^[\s]*(accept|reject)\s*(all\s*)?cookies[\s]*$', re.I | re.MULTILINE),
    ]
    
    # Unicode replacements
    UNICODE_REPLACEMENTS = {
        '\u2019': "'",  # Right single quote
        '\u2018': "'",  # Left single quote
        '\u201c': '"',  # Left double quote
        '\u201d': '"',  # Right double quote
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        '\u2026': '...',  # Ellipsis
        '\u00a0': ' ',  # Non-breaking space
        '\u200b': '',   # Zero-width space
        '\ufeff': '',   # BOM
    }
    
    @classmethod
    def clean_job_text(cls, raw_text: str) -> str:
        """
        Clean job description text.
        
        - Strip HTML tags
        - Normalize unicode characters
        - De-boilerplate scrub (remove UI junk)
        - Normalize whitespace
        - Preserve bullet points and list structure
        """
        if not raw_text:
            return ""
        
        text = raw_text
        
        # Unescape HTML entities first
        text = unescape(text)
        
        # Remove HTML tags but preserve line breaks
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<p\s*/?>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</p>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<li\s*>', '\n• ', text, flags=re.IGNORECASE)
        text = cls.HTML_TAG_PATTERN.sub('', text)
        
        # Normalize unicode
        for old, new in cls.UNICODE_REPLACEMENTS.items():
            text = text.replace(old, new)
        
        # De-boilerplate scrub - remove common job board UI junk
        for pattern in cls.BOILERPLATE_PATTERNS:
            text = pattern.sub('', text)
        
        # Normalize whitespace (preserve newlines for structure)
        text = cls.MULTI_SPACE_PATTERN.sub(' ', text)
        text = cls.MULTI_NEWLINE_PATTERN.sub('\n\n', text)
        
        # Clean up lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text.strip()
    
    @classmethod
    def clean_resume_text(cls, raw_text: str) -> str:
        """
        Clean resume text from PDF extraction.
        
        Similar to job text but handles common PDF artifacts.
        """
        if not raw_text:
            return ""
        
        text = raw_text
        
        # PDF-specific cleanup
        # Remove page numbers (common patterns)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        text = re.sub(r'\n\s*Page\s+\d+\s*(of\s+\d+)?\s*\n', '\n', text, flags=re.IGNORECASE)
        
        # Remove header/footer artifacts (repeated text)
        # This is a simplified heuristic
        
        # Normalize unicode
        for old, new in cls.UNICODE_REPLACEMENTS.items():
            text = text.replace(old, new)
        
        # Normalize whitespace
        text = cls.MULTI_SPACE_PATTERN.sub(' ', text)
        text = cls.MULTI_NEWLINE_PATTERN.sub('\n\n', text)
        
        # Clean up lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(line for line in lines if line)
        
        return text.strip()


class JobMetadataExtractor:
    """Extract metadata from job descriptions using heuristics and patterns."""
    
    # Seniority patterns
    SENIORITY_PATTERNS = {
        'intern': re.compile(r'\b(intern|internship)\b', re.I),
        'junior': re.compile(r'\b(junior|jr\.?|entry[\s-]?level|associate)\b', re.I),
        'mid': re.compile(r'\b(mid[\s-]?level|intermediate)\b', re.I),
        'senior': re.compile(r'\b(senior|sr\.?)\b', re.I),
        'staff': re.compile(r'\b(staff)\b', re.I),
        'principal': re.compile(r'\b(principal)\b', re.I),
        'lead': re.compile(r'\b(lead|tech\s*lead)\b', re.I),
        'manager': re.compile(r'\b(manager|engineering\s*manager)\b', re.I),
        'director': re.compile(r'\b(director)\b', re.I),
        'vp': re.compile(r'\b(vp|vice\s*president)\b', re.I),
    }
    
    # Role type patterns
    ROLE_PATTERNS = {
        'backend': re.compile(r'\b(backend|back[\s-]?end|server[\s-]?side)\b', re.I),
        'frontend': re.compile(r'\b(frontend|front[\s-]?end|ui|user\s*interface)\b', re.I),
        'fullstack': re.compile(r'\b(fullstack|full[\s-]?stack)\b', re.I),
        'devops': re.compile(r'\b(devops|dev[\s-]?ops|platform\s*engineer)\b', re.I),
        'sre': re.compile(r'\b(sre|site\s*reliability)\b', re.I),
        'data_engineer': re.compile(r'\b(data\s*engineer)\b', re.I),
        'data_scientist': re.compile(r'\b(data\s*scien(tist|ce))\b', re.I),
        'ml_engineer': re.compile(r'\b(ml|machine\s*learning)\s*(engineer)?\b', re.I),
        'mobile': re.compile(r'\b(mobile|ios|android)\b', re.I),
        'security': re.compile(r'\b(security|infosec|cybersecurity)\b', re.I),
        'qa': re.compile(r'\b(qa|quality\s*assurance|test|sdet)\b', re.I),
    }
    
    # Remote patterns
    REMOTE_PATTERNS = {
        'remote': re.compile(r'\b(fully?\s*remote|100%\s*remote|remote\s*only)\b', re.I),
        'hybrid': re.compile(r'\b(hybrid|flex|flexible\s*location)\b', re.I),
        'onsite': re.compile(r'\b(on[\s-]?site|in[\s-]?office|office[\s-]?based)\b', re.I),
    }
    
    # Salary patterns
    SALARY_PATTERN = re.compile(
        r'\$\s*(\d{2,3})[,.]?(\d{3})?\s*[-–to]+\s*\$?\s*(\d{2,3})[,.]?(\d{3})?'
        r'|\$\s*(\d{2,3})[kK]\s*[-–to]+\s*\$?\s*(\d{2,3})[kK]',
        re.I
    )
    
    # Title extraction patterns (first line often contains title)
    TITLE_PATTERN = re.compile(
        r'^(.{10,100}?(engineer|developer|architect|scientist|manager|director|lead|analyst|designer))',
        re.I | re.MULTILINE
    )
    
    @classmethod
    def extract_metadata(cls, text: str, title_hint: Optional[str] = None) -> JobMetadata:
        """
        Extract metadata from job description text.
        
        """
        metadata = JobMetadata()
        
        # Use first 500 chars for title/company (usually in header)
        header = text[:500] if len(text) > 500 else text
        
        # Extract title
        if title_hint:
            metadata.title = title_hint
        else:
            title_match = cls.TITLE_PATTERN.search(header)
            if title_match:
                metadata.title = title_match.group(1).strip()
        
        # Extract seniority (check full text)
        for level, pattern in cls.SENIORITY_PATTERNS.items():
            if pattern.search(text):
                metadata.seniority = level
                break
        
        # Extract role type
        for role, pattern in cls.ROLE_PATTERNS.items():
            if pattern.search(text):
                metadata.role_type = role
                break
        
        # Extract remote type
        for remote_type, pattern in cls.REMOTE_PATTERNS.items():
            if pattern.search(text):
                metadata.remote_type = remote_type
                break
        
        # Extract salary
        salary_match = cls.SALARY_PATTERN.search(text)
        if salary_match:
            groups = salary_match.groups()
            try:
                if groups[0]:  # Full number format: $120,000 - $150,000
                    min_val = int(groups[0]) * (1000 if groups[1] else 1)
                    if groups[1]:
                        min_val = int(groups[0] + groups[1])
                    max_val = int(groups[2]) * (1000 if groups[3] else 1)
                    if groups[3]:
                        max_val = int(groups[2] + groups[3])
                    metadata.salary_min = min_val
                    metadata.salary_max = max_val
                elif groups[4]:  # K format: $120K - $150K
                    metadata.salary_min = int(groups[4]) * 1000
                    metadata.salary_max = int(groups[5]) * 1000
                metadata.salary_currency = "USD"
            except (ValueError, TypeError):
                pass
        
        return metadata


class JobSectionExtractor:
    """Extract sections from job descriptions."""
    
    # Section header patterns
    REQUIREMENTS_HEADERS = re.compile(
        r'^[\s•\-\*]*'
        r'(requirements?|qualifications?|what\s*you.*(need|bring)|must[\s-]?have|minimum\s*qualifications?)'
        r'[\s:]*$',
        re.I | re.MULTILINE
    )
    
    NICE_TO_HAVE_HEADERS = re.compile(
        r'^[\s•\-\*]*'
        r'(nice[\s-]?to[\s-]?have|preferred|bonus|plus|desired|additional)'
        r'[\s:]*$',
        re.I | re.MULTILINE
    )
    
    RESPONSIBILITIES_HEADERS = re.compile(
        r'^[\s•\-\*]*'
        r'(responsibilities|what\s*you.*(do|work)|role|duties|the\s*job)'
        r'[\s:]*$',
        re.I | re.MULTILINE
    )
    
    BENEFITS_HEADERS = re.compile(
        r'^[\s•\-\*]*'
        r'(benefits|perks|what\s*we\s*offer|compensation|why\s*(join|work))'
        r'[\s:]*$',
        re.I | re.MULTILINE
    )
    
    # Generic section end pattern
    SECTION_END = re.compile(
        r'^[\s•\-\*]*'
        r'(about|requirements?|qualifications?|responsibilities|benefits|perks|nice[\s-]?to|preferred|'
        r'what\s*you|what\s*we|the\s*team|our\s*company|how\s*to\s*apply)'
        r'[\s:]*$',
        re.I | re.MULTILINE
    )
    
    @classmethod
    def extract_sections(cls, text: str) -> ExtractedSections:
        """Extract major sections from job description."""
        sections = ExtractedSections()
        
        sections.requirements = cls._extract_section(text, cls.REQUIREMENTS_HEADERS)
        sections.nice_to_have = cls._extract_section(text, cls.NICE_TO_HAVE_HEADERS)
        sections.responsibilities = cls._extract_section(text, cls.RESPONSIBILITIES_HEADERS)
        sections.benefits = cls._extract_section(text, cls.BENEFITS_HEADERS)
        
        return sections
    
    @classmethod
    def _extract_section(cls, text: str, header_pattern: re.Pattern) -> Optional[str]:
        """Extract a section starting from header pattern."""
        match = header_pattern.search(text)
        if not match:
            return None
        
        start = match.end()
        
        # Find next section header
        remaining = text[start:]
        end_match = cls.SECTION_END.search(remaining)
        
        if end_match:
            section_text = remaining[:end_match.start()]
        else:
            # Take up to 2000 chars if no clear end
            section_text = remaining[:2000]
        
        return section_text.strip() if section_text.strip() else None


def clean_and_parse_job(raw_text: str, title: Optional[str] = None) -> dict:
    """
    Full job text processing pipeline.
    """
    cleaned = TextCleaner.clean_job_text(raw_text)
    metadata = JobMetadataExtractor.extract_metadata(cleaned, title)
    sections = JobSectionExtractor.extract_sections(cleaned)
    
    return {
        "cleaned_text": cleaned,
        "metadata": {
            "title": metadata.title,
            "company": metadata.company,
            "location": metadata.location,
            "seniority": metadata.seniority,
            "role_type": metadata.role_type,
            "remote_type": metadata.remote_type,
            "salary_min": metadata.salary_min,
            "salary_max": metadata.salary_max,
            "salary_currency": metadata.salary_currency,
        },
        "sections": {
            "requirements": sections.requirements,
            "nice_to_have": sections.nice_to_have,
            "responsibilities": sections.responsibilities,
            "benefits": sections.benefits,
        }
    }