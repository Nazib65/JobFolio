"""
Analysis related pydantic schemas
"""

from datetime import datetime 
from typing import Optional

from apps.api.app.schemas.skill import UserSkillResponse
from pydantic import BaseModel, Field

from .base import BaseSchema, IDMixin, TimeStampMixin

#===============
# Request Schemas 
#===============

class AnalysisCreate(BaseModel):
    """ Request to create a neew analysis """
    job_id: int 
    resume_id: Optional[int] = None 

class AnalysisQuestion(BaseModel):
    """ Question for Q&A about analysis """
    question: str = Field(..., min_length=5, max_length=500)

# ===================
# JSON Detail Sub-Schemas
# These define the structure of analysis.json_detail
# ===================

class RadarScores(BaseModel):
    """
    Category scores for radar charrt visualization.
    Each score is 0-100. 
    """

    backend: float = Field(..., ge=0, le=100)
    frontend: float = Field(..., ge=0, le=100)
    devops: float = Field(..., ge=0, le=100)
    ml_ai: float = Field(..., ge=0, le=100)
    communication: float = Field(..., ge=0, le=100)

    # Optional additional categories 
    data: Optional[float] = Field(None, ge=0, le=100)
    mobile: Optional[float] = Field(None, ge=0, le=100)
    security: Optional[float] = Field(None, ge=0, le=100)
class EvidenceItem(BaseModel):
    """ Evidence llinking a user to source material """
    source: str 
    text: str 
    context: Optional[str] = None 
    repo_name: Optional[str] = None 
    similarity_score: float= Field(..., ge=0, le=1)

class SkillTableRow(BaseModel):
    """ 
    Single row in he skills analysis table.
    Maps required job skills to user evidence.
    """
    skill_id: int 
    skill_name: str 
    category: str   # language/framework/ tool/soft-skill/etc

    # job side
    required: bool # True if skill is required, False if nice_to_have
    strength: float= Field(..., ge=0, le=1) # User's stregth in this sill
    user_years: Optional[float] = None 

    # Evidence 
    evidence: list[EvidenceItem] = []
    best_evidence_preview: Optional[str] = None # Short preview for table display 

class LearningResource(BaseModel):
    """ A suggested learning resource for a skill gap """
    type: str # "coourse" | "doocumentation" | "tutorial"  | " book" | "video"
    title:str 
    provider: Optional[str] = None # "Coursera", "Udemy", "official docs"
    url: Optional[str] = None 
    duration: Optional[str] = None # "4 weeks", "2 hours"
    difficulty: Optional[str] = None # "beginner | "intermediate" | "advanced
    is_free: Optional[bool] = None

class GapRoadmapItem(BaseModel):
    """
    Roadmap item for closing a skill gap
    """
    skill_id: int 
    skill_name: str 
    category: str 
    importance: int # How importance for this job 
    current_strength: float # User's current level
    target_strength: float #Recommedned level for this job 

    # Explanation
    why_it_matters: str 

    # learning path
    resources: list[LearningResource] 
    estimated_time: Optional[str] = None 

    # Project suggestion
    project_idea = str
    project_skills_pracrticed: list[str] = []

class BonusSkillItem(BaseModel):
    """ Extra skill that user has that is not required but not relevant """
    skill_id: int 
    skill_name: str
    category: str 
    strength: float
    relavance_note: str # "Valuable for future growth in ML roles"

class ScoreBreakdown(BaseModel):
    """
    Detailed breakdown of how sscores were calculated
    """
    # Coverage calculation
    total_required_skills: int 
    matched_skills: int 
    partial_skills: int 
    missing_skills: int 
    coverage_formula: str # "matched + 0.5*partial/ total"

    # Depth calculation 
    top_skills_evaluated: int 
    average_evidence_strength: float
    depth_formula: str 

    # Bonus calculation
    bonus_skills_count: int
    bonus_relevance_average: float

    # Weight used
    weights: dict[str, float] # {"coverage":0.6, "depth":0.4, "bonus":0.2}

class AnalysisJsonDetail(BaseModel):
    """
    Complete JSON detail structure for an analysis.
    This is the main contract between backend and frontend.
    """

    # Version for schema evoulution
    schema_version: str ="1.0"

    # Scores(0-100)
    overall_score: float = Field(..., ge=0, le=100)
    coverage_score: float = Field(..., ge=0, le=100)
    depth_score: float = Field(..., ge=0, le=100)
    bonus_score: float = Field(..., ge=0, le=100)

    # Radar chart data 
    radar: RadarScores

    # Skills table (main analysis view)
    skills_table: list[SkillTableRow]

    # Score breakdown for ttransparency 
    score_breakdown: ScoreBreakdown 

    # Gap analysis and roadmap
    gaps: list[GapRoadmapItem]

    # Bonus skills 
    bonus_skills: list[BonusSkillItem]

    # Quick summaries
    top_strengths: list[str] # Python, Rest APIs, Docker
    top_gaps: list[str] # Kubernetes, React, Go

    # AI - generated narrative
    file_summary: str # 2-3 sentence summary 
    strength_narrative: str # Paragrapgh about strengths
    gaps_narrative: str # Paragraph about gaps and next steps 

    # Metadata 
    job_id: int 
    job_title: str 
    company: Optional[str] = None 
    resume_id: Optional[int] = None
    analyzed_at: datetime
    model_version: str  # e.g., "ML model v1.2", "GPT-5.0"

# ===================
# Response Schemas
# ===================

class AnalysisBase(BaseSchema, IDMixin):
    """ Base analysis response """
    job_id: int 
    status: str # pending, in_progress, completed, failed
    overall_score: Optional[float] = None 
    coverage_score: Optional[float] = None 
    depth_score: Optional[float] = None

class AnalysisSummary(AnalysisBase, TimeStampMixin):
    """ Analysis summary for listings """
    job_title: str 
    company: Optional[str] = None 
    top_strengths: Optional[list[str]] = None
    top_gaps: Optional[list[str]] = None

class AnalysisResponse(AnalysisBase, TimeStampMixin):
    """ Full analysis response with details"""
    bonus_score: Optional[float] = None 
    summary: Optional[str] = None 
    top_strengths: list[str]  = [] 
    top_gaps: list[str] = []
    processing_error: Optional[str] = None 
    proccessing_time_ms: Optional[int] = None 

    # The complere analysis detail JSON
    json_detail: Optional[AnalysisJsonDetail] =  None 

class AnalysisProcessingStatus(BaseModel):
    """ Analysis Processing Status """
    analysis_id: int 
    status: str 
    progress: Optional[int] = None # 0-100
    current_step: Optional[str] = None 
    error: Optional[str] = None

class QuestionAnswe(BaseModel):
    """ Response to a Q&A question about the analysis """
    question: str 
    answer: str
    relevant_skills: list[str] = []
    confidence: float # 0-1

class AnalysisComparison(BaseModel):
    """Comparison of multiple analyses """
    analyses: list[AnalysisSummary]
    best_fit_job_id: int 
    comaprison_notes: str
    skill_coverage_comaprison: dict[str, dict[int, float]] # skill_name -> {job_id -> score}

# Export for FrontEnd

class FrontendAnalysisPayload(BaseModel):
    """Complete payload sent to fronend for rendering analysis page"""

    analysis: AnalysisResponse
    job: "JobDetail" # Foeward reference
    user_skills: list["UserSkillResponse"] # Forward reference

    class Config:
        from_attributes = True
    
from .job import JobDetail
from .skill import UserSkillResponse

FrontendAnalysisPayload.model_rebuild()