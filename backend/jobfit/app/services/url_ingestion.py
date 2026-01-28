"""
URL ingestion service for fetching job descriptions from URLs.

Handles:
- HTML fetching with proper headers
- JavaScript-rendered page detection
- Fallback messaging for blocked/JS-only pages
- Basic HTML parsing to extract job content
"""
import re
import logging
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class URLIngestResult:
    """Result of URL ingestion attempt."""
    success: bool
    raw_text: Optional[str] = None
    raw_html: Optional[str] = None
    source_url: str = ""
    detected_platform: Optional[str] = None  # greenhouse, lever, workday, linkedin, etc.
    requires_js: bool = False
    is_blocked: bool = False
    error_message: Optional[str] = None
    fallback_message: Optional[str] = None
    # Debug/quality fields
    content_length: int = 0
    fetch_time_ms: int = 0
    http_status: Optional[int] = None


class URLIngestService:
    """
    Service for fetching and parsing job descriptions from URLs.
    """
    
    # Common job board/ATS patterns
    PLATFORM_PATTERNS = {
        'greenhouse': re.compile(r'(greenhouse\.io|boards\.greenhouse)', re.I),
        'lever': re.compile(r'(lever\.co|jobs\.lever)', re.I),
        'workday': re.compile(r'(workday\.com|myworkdayjobs)', re.I),
        'linkedin': re.compile(r'linkedin\.com/jobs', re.I),
        'indeed': re.compile(r'indeed\.com', re.I),
        'glassdoor': re.compile(r'glassdoor\.com', re.I),
        'angellist': re.compile(r'(angel\.co|wellfound\.com)', re.I),
        'ashby': re.compile(r'ashbyhq\.com', re.I),
        'bamboohr': re.compile(r'bamboohr\.com', re.I),
        'smartrecruiters': re.compile(r'smartrecruiters\.com', re.I),
    }
    
    # Platforms known to require JavaScript
    JS_REQUIRED_PLATFORMS = {'linkedin', 'indeed', 'glassdoor', 'workday'}
    
    # Common selectors for job content
    JOB_CONTENT_SELECTORS = [
        # Greenhouse
        ('div#content', 'greenhouse'),
        ('div.job-post-content', 'greenhouse'),
        # Lever
        ('div.posting-page', 'lever'),
        ('div.content', 'lever'),
        # Generic
        ('article.job-description', None),
        ('div.job-description', None),
        ('div.description', None),
        ('main', None),
        ('article', None),
    ]
    
    # Elements to remove (navigation, footers, etc.)
    REMOVE_SELECTORS = [
        'header', 'footer', 'nav', 'aside',
        '.nav', '.navigation', '.menu',
        '.header', '.footer', '.sidebar',
        '.cookie-banner', '.cookie-consent',
        '.social-share', '.share-buttons',
        '.apply-button', '.apply-now',
        'script', 'style', 'noscript',
    ]
    
    def __init__(
        self,
        timeout: float = 15.0,
        max_content_length: int = 500_000,  # 500KB
    ):
        self.timeout = timeout
        self.max_content_length = max_content_length
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
    
    async def ingest_url(self, url: str) -> URLIngestResult:
        """
        Attempt to fetch and parse a job description from a URL.
        """
        import time
        start_time = time.time()
        
        # Validate URL
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return URLIngestResult(
                    success=False,
                    source_url=url,
                    error_message="Invalid URL format",
                    fallback_message="Please provide a valid URL starting with http:// or https://",
                )
        except Exception:
            return URLIngestResult(
                success=False,
                source_url=url,
                error_message="Could not parse URL",
                fallback_message="Please provide a valid URL",
            )
        
        # Detect platform
        platform = self._detect_platform(url)
        
        # Check if known JS-only platform
        if platform in self.JS_REQUIRED_PLATFORMS:
            return URLIngestResult(
                success=False,
                source_url=url,
                detected_platform=platform,
                requires_js=True,
                fallback_message=f"This {platform.title()} job page requires JavaScript to load. Please copy and paste the job description text directly.",
            )
        
        # Attempt to fetch
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
                headers=self.headers,
            ) as client:
                response = await client.get(url)
                
                fetch_time_ms = int((time.time() - start_time) * 1000)
                
                # Check response
                if response.status_code == 403:
                    return URLIngestResult(
                        success=False,
                        source_url=url,
                        detected_platform=platform,
                        is_blocked=True,
                        http_status=403,
                        fetch_time_ms=fetch_time_ms,
                        fallback_message="Access denied by the website. Please copy and paste the job description text directly.",
                    )
                
                if response.status_code == 404:
                    return URLIngestResult(
                        success=False,
                        source_url=url,
                        detected_platform=platform,
                        http_status=404,
                        fetch_time_ms=fetch_time_ms,
                        error_message="Job posting not found (404)",
                        fallback_message="This job posting may have been removed. Please check the URL or paste the job description directly.",
                    )
                
                if response.status_code != 200:
                    return URLIngestResult(
                        success=False,
                        source_url=url,
                        detected_platform=platform,
                        http_status=response.status_code,
                        fetch_time_ms=fetch_time_ms,
                        error_message=f"HTTP {response.status_code}",
                        fallback_message="Could not access this page. Please copy and paste the job description text directly.",
                    )
                
                # Check content length
                content_length = len(response.content)
                if content_length > self.max_content_length:
                    return URLIngestResult(
                        success=False,
                        source_url=url,
                        detected_platform=platform,
                        http_status=200,
                        content_length=content_length,
                        fetch_time_ms=fetch_time_ms,
                        error_message="Page too large",
                        fallback_message="This page is too large to process. Please copy and paste the job description text directly.",
                    )
                
                raw_html = response.text
                
                # Parse HTML and extract text
                raw_text = self._extract_job_text(raw_html, platform)
                
                # Check if we got meaningful content
                if not raw_text or len(raw_text.strip()) < 100:
                    return URLIngestResult(
                        success=False,
                        source_url=url,
                        detected_platform=platform,
                        raw_html=raw_html[:10000] if raw_html else None,  # Store partial for debugging
                        http_status=200,
                        content_length=content_length,
                        fetch_time_ms=fetch_time_ms,
                        requires_js=True,  # Likely JS-rendered
                        fallback_message="This page appears to require JavaScript to display content. Please copy and paste the job description text directly.",
                    )
                
                return URLIngestResult(
                    success=True,
                    raw_text=raw_text,
                    raw_html=raw_html,
                    source_url=url,
                    detected_platform=platform,
                    http_status=200,
                    content_length=content_length,
                    fetch_time_ms=fetch_time_ms,
                )
                
        except httpx.TimeoutException:
            return URLIngestResult(
                success=False,
                source_url=url,
                detected_platform=platform,
                fetch_time_ms=int(self.timeout * 1000),
                error_message="Request timed out",
                fallback_message="The page took too long to load. Please copy and paste the job description text directly.",
            )
        except httpx.RequestError as e:
            logger.error(f"Request error for {url}: {e}")
            return URLIngestResult(
                success=False,
                source_url=url,
                detected_platform=platform,
                error_message=str(e),
                fallback_message="Could not connect to this website. Please copy and paste the job description text directly.",
            )
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            return URLIngestResult(
                success=False,
                source_url=url,
                detected_platform=platform,
                error_message=str(e),
                fallback_message="An error occurred while fetching this page. Please copy and paste the job description text directly.",
            )
    
    def _detect_platform(self, url: str) -> Optional[str]:
        """Detect the job board/ATS platform from URL."""
        for platform, pattern in self.PLATFORM_PATTERNS.items():
            if pattern.search(url):
                return platform
        return None
    
    def _extract_job_text(self, html: str, platform: Optional[str] = None) -> str:
        """
        Extract job description text from HTML.
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove unwanted elements
            for selector in self.REMOVE_SELECTORS:
                for element in soup.select(selector):
                    element.decompose()
            
            # Try platform-specific and generic selectors
            content = None
            for selector, selector_platform in self.JOB_CONTENT_SELECTORS:
                # Skip platform-specific selectors for other platforms
                if selector_platform and selector_platform != platform:
                    continue
                
                elements = soup.select(selector)
                if elements:
                    content = elements[0]
                    break
            
            # Fallback to body
            if not content:
                content = soup.body or soup
            
            # Extract text with some structure preservation
            text = self._extract_text_with_structure(content)
            
            return text
            
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return ""
    
    def _extract_text_with_structure(self, element) -> str:
        """
        Extract text while preserving some structure (lists, paragraphs).
        """
        lines = []
        
        for child in element.descendants:
            if child.name in ['p', 'div', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                lines.append('\n')
            elif child.name == 'li':
                lines.append('\n• ')
            elif child.string:
                text = child.string.strip()
                if text:
                    lines.append(text + ' ')
        
        text = ''.join(lines)
        
        # Clean up whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r' \n', '\n', text)
        text = re.sub(r'\n ', '\n', text)
        
        return text.strip()


# Singleton instance
url_ingest_service = URLIngestService()