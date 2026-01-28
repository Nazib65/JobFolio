"""
GitHub API client for fetching repository information.
"""
import re
import base64
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass
class GitHubRepo:
    """GitHub repository data."""
    repo_id: int
    full_name: str  # owner/repo
    name: str
    description: Optional[str]
    url: str
    
    # Metrics
    stars_count: int
    forks_count: int
    watchers_count: int
    
    # Languages
    languages: dict[str, int]  # language -> bytes
    primary_language: Optional[str]
    
    # Metadata
    is_fork: bool
    is_private: bool
    topics: list[str]
    
    # README content
    readme_content: Optional[str] = None
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    pushed_at: Optional[datetime] = None
    
    # Errors during fetch
    errors: list[str] = field(default_factory=list)


class GitHubClient:
    """
    Async client for GitHub API.
    """
    
    BASE_URL = "https://api.github.com"
    
    # Repo URL patterns
    GITHUB_URL_PATTERN = re.compile(
        r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/\s?#]+)/?',
        re.I
    )
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub client.
        
        Args:
            token: Optional personal access token for higher rate limits
        """
        self.token = token or settings.github_api_token
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "JobFit-Copilot/1.0",
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
    
    @classmethod
    def parse_repo_url(cls, url: str) -> Optional[tuple[str, str]]:
        """
        Parse GitHub URL to extract owner and repo name.
        """
        # Clean the URL
        url = url.strip().rstrip('/')
        
        # Remove .git suffix
        if url.endswith('.git'):
            url = url[:-4]
        
        match = cls.GITHUB_URL_PATTERN.search(url)
        if match:
            return match.group(1), match.group(2)
        
        return None
    
    async def fetch_repo(self, owner: str, repo: str) -> GitHubRepo:
        """
        Fetch repository information.
        """
        errors = []
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Fetch repo metadata
            repo_data = await self._fetch_repo_metadata(client, owner, repo)
            if not repo_data:
                return GitHubRepo(
                    repo_id=0,
                    full_name=f"{owner}/{repo}",
                    name=repo,
                    description=None,
                    url=f"https://github.com/{owner}/{repo}",
                    stars_count=0,
                    forks_count=0,
                    watchers_count=0,
                    languages={},
                    primary_language=None,
                    is_fork=False,
                    is_private=True,
                    topics=[],
                    errors=["Repository not found or not accessible"],
                )
            
            # Fetch languages
            languages = await self._fetch_languages(client, owner, repo)
            
            # Fetch README
            readme_content = await self._fetch_readme(client, owner, repo)
            
            # Parse timestamps
            created_at = self._parse_timestamp(repo_data.get('created_at'))
            updated_at = self._parse_timestamp(repo_data.get('updated_at'))
            pushed_at = self._parse_timestamp(repo_data.get('pushed_at'))
            
            return GitHubRepo(
                repo_id=repo_data.get('id', 0),
                full_name=repo_data.get('full_name', f"{owner}/{repo}"),
                name=repo_data.get('name', repo),
                description=repo_data.get('description'),
                url=repo_data.get('html_url', f"https://github.com/{owner}/{repo}"),
                stars_count=repo_data.get('stargazers_count', 0),
                forks_count=repo_data.get('forks_count', 0),
                watchers_count=repo_data.get('watchers_count', 0),
                languages=languages,
                primary_language=repo_data.get('language'),
                is_fork=repo_data.get('fork', False),
                is_private=repo_data.get('private', False),
                topics=repo_data.get('topics', []),
                readme_content=readme_content,
                created_at=created_at,
                updated_at=updated_at,
                pushed_at=pushed_at,
                errors=errors,
            )
    
    async def fetch_repo_from_url(self, url: str) -> Optional[GitHubRepo]:
        """
        Fetch repository from URL.
        """
        parsed = self.parse_repo_url(url)
        if not parsed:
            return None
        
        owner, repo = parsed
        return await self.fetch_repo(owner, repo)
    
    async def fetch_multiple_repos(self, urls: list[str]) -> list[GitHubRepo]:
        """
        Fetch multiple repositories.
        """
        results = []
        
        for url in urls:
            try:
                repo = await self.fetch_repo_from_url(url)
                if repo:
                    results.append(repo)
                else:
                    # Create error result for invalid URL
                    results.append(GitHubRepo(
                        repo_id=0,
                        full_name=url,
                        name="invalid",
                        description=None,
                        url=url,
                        stars_count=0,
                        forks_count=0,
                        watchers_count=0,
                        languages={},
                        primary_language=None,
                        is_fork=False,
                        is_private=False,
                        topics=[],
                        errors=[f"Invalid GitHub URL: {url}"],
                    ))
            except Exception as e:
                logger.error(f"Error fetching {url}: {e}")
                results.append(GitHubRepo(
                    repo_id=0,
                    full_name=url,
                    name="error",
                    description=None,
                    url=url,
                    stars_count=0,
                    forks_count=0,
                    watchers_count=0,
                    languages={},
                    primary_language=None,
                    is_fork=False,
                    is_private=False,
                    topics=[],
                    errors=[f"Fetch error: {str(e)}"],
                ))
        
        return results
    
    async def _fetch_repo_metadata(
        self, client: httpx.AsyncClient, owner: str, repo: str
    ) -> Optional[dict]:
        """Fetch repository metadata."""
        try:
            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}",
                headers=self.headers,
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.warning(f"Repository not found: {owner}/{repo}")
                return None
            elif response.status_code == 403:
                logger.error(f"GitHub API rate limit exceeded")
                return None
            else:
                logger.error(f"GitHub API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching repo metadata: {e}")
            return None
    
    async def _fetch_languages(
        self, client: httpx.AsyncClient, owner: str, repo: str
    ) -> dict[str, int]:
        """Fetch repository languages."""
        try:
            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}/languages",
                headers=self.headers,
            )
            
            if response.status_code == 200:
                return response.json()
            return {}
            
        except Exception as e:
            logger.error(f"Error fetching languages: {e}")
            return {}
    
    async def _fetch_readme(
        self, client: httpx.AsyncClient, owner: str, repo: str
    ) -> Optional[str]:
        """Fetch repository README content."""
        try:
            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}/readme",
                headers=self.headers,
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get('content', '')
                encoding = data.get('encoding', 'base64')
                
                if encoding == 'base64' and content:
                    try:
                        decoded = base64.b64decode(content).decode('utf-8')
                        # Truncate if too long
                        if len(decoded) > 10000:
                            decoded = decoded[:10000] + "\n\n[README truncated...]"
                        return decoded
                    except Exception:
                        return None
                return content
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching README: {e}")
            return None
    
    @staticmethod
    def _parse_timestamp(ts: Optional[str]) -> Optional[datetime]:
        """Parse ISO timestamp from GitHub API."""
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts.replace('Z', '+00:00'))
        except Exception:
            return None
    
    async def check_rate_limit(self) -> dict:
        """Check current rate limit status."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.BASE_URL}/rate_limit",
                headers=self.headers,
            )
            
            if response.status_code == 200:
                data = response.json()
                core = data.get('resources', {}).get('core', {})
                return {
                    "limit": core.get('limit', 0),
                    "remaining": core.get('remaining', 0),
                    "reset_at": datetime.fromtimestamp(core.get('reset', 0)),
                    "authenticated": self.token is not None,
                }
            
            return {"error": "Unable to fetch rate limit"}


# Singleton instance for use without explicit initialization
github_client = GitHubClient()