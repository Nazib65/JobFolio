"""
Skill Realted pydanctic schemas.
"""
from typing import Optional
from pydantic import BaseModel, Field
from .base import BaseSchema, IDMixin, TimestampMixin   

# ===================
# Request Schemas
# ===================
class SkillCreate(BaseModel):
    """ Schema for creating a new canonical skill """
    cnanonical_name: str = Field(..., min_length=1, max_length=100)
    display_name: str =Field(..., min_length=1, max_lenght=100)
    category: str
    subcategory: Optional[str]=None 
    aliases: list[str]=[]
    description: Optional[str]=None 
    documentation_url: Optional[str]=None 

class SkillUpdate(BaseModel):
    """ Schema for updating a skill """
    display_name: Optional[str]=Field(None, max_length=100)
    category: Optional[str]=None 
    subcategory: Optional[str]=None 
    aliases: Optional[list[str]]=None 
    description: Optional[str]=None
    is_trending: Optional[bool]=None 

class UserSkillUpdate(BaseModel):
    """ Schema for user updating their skill profile """
    self_reported_level: Optional[str]=Field(None, pattern="^(beginner|intermediate|advanced|expert)$")
    is_learning: Optional[bool]=None 
    notes: Optional[str]=Field(None, max_length=1000)

# ===================
# Response Schemas
# ===================

class SkillBase(BaseSchema, IDMixin):
    """ Base Skill Response Schema """
    canonical_name: str
    display_name: str
    category: str
    subcategory: Optional[str]=None 

class SkillSummary(SkillBase):
    """ Skill Summary """
    icon_url: Optional[str]=None 
    is_trending: bool=False

class SkillDetail(SkillBase, TimestampMixin):
    """ Full Skill detail"""
    aliases: list[str]=[]
    related_skills: list[str]=[]
    description: Optional[str]=None 
    icon_url: Optional[str]=None 
    documentation_url: Optional[str]=None
    is_trending: bool=False
    market_demand_score: Optional[float]=None 

class UserSkillResponse(BaseModel):
    """ User's skill with evidence """
    skill_id: int
    skill_name: str
    category: str
    strength: float
    primary_source: str
    years_experience: Optional[float]=None 
    self_reported_level: Optional[str]=None 
    is_learning: bool=False
    best_evidence_text: Optional[str]=None 
    evidence_count: int=0

class UserSkillDetail(UserSkillResponse, TimestampMixin):
    """ Detailed User skill with all evidence """
    evidence: list[dict]=[]
    notes: Optional[str]=None 

class SkillCategory(BaseModel):
    """ Skill category with counts """
    category: str
    display_name: str
    skills_count: int 
    user_skills_count: int 

class SkillSearchResult(BaseModel):
    """ Skill search result """
    skill_id: int 
    canonical_name: str
    display_name: str
    category: str
    match_type: str # e.g., 'exact', 'partial', 'alias'
    match_score: float 
    

