"""
User related pydantic schemas
"""
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from .base import BaseSchema, IDMixin, TimestampMixin

# ===================
# Request Schemas
# ===================

class UserCreate(BaseModel):
    """ Schema for creating a new user """
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """ Schema for updating user profile """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    headline: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = Field(None, max_length=2000)
    location: Optional[str] = Field(None, max_length=255)

class UserLogin(BaseModel):
    """ Schema for user login """
    email: EmailStr
    Password: str

class GitHubConnectRequest(BaseModel):
    """ Schema for initiating github OAuth. """
    redirect_uri: Optional[str] = None 

class GutHubCallbackRequest(BaseModel):
    """ Schema for Github OAuth callback. """
    code: str 
    state: str

#==============
# Response Schema 
#==============

class UserBase(BaseModel, IDMixin):
    """ Base user response schema """
    email: str 
    name: str 
    headline: Optional[str] = None 
    location: Optional[str] = None 
    avatar_url: Optional[str] = None 

class UserResponse(UserBase, TimestampMixin):
    """ Full user response schema """
    bio: Optional[str] = None 
    github_username: Optional[str]= None 
    github_connected_at: Optional[datetime] = None 
    is_verified: bool =False

class UserPublicProfile(UserBase): 
    """ Public profile schema( limited info). """
    pass

class GithubConnectResponse(BaseModel):
    """ Response for github OAuth initiation """
    authorization_url: str 
    state: str

class GithubConnecctionStatus(BaseModel):
    """ Status for github connection """
    connection: bool 
    username: Optional[str] = None 
    connected_at: Optional[datetime] = None 
    repos_count: Optional[int] = None 

class AuthTokenResponse(BaseModel): 
    """ Authentication token response """
    access_token: str 
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None 

class UserStats(BaseModel):
    """ User statisstics """
    resumes_count: int 
    projects_count: int 
    analyses_count: int 
    skills_count: int  
