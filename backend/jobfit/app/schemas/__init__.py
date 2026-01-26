"""
Pydantic schemas for JobFit Copilot API.

All request/response schemas are defined here for API contracts.
"""
from .base import (
    BaseSchema,
    PaginationParams,
    PaginatedResponse,
    ErrorResponse,
    SuccessResponse,
)

from .user import (
    UserCreate,
    UserUpdate,
    UserLogin,
    GitHubConnectRequest,
    GitHubCallbackRequest,
    UserResponse,
    UserPublicProfile,
    GitHubConnectResponse,
    GitHubConnectionStatus,
    AuthTokenResponse,
    UserStats,
)

from .job import (
    JobCreate,
    JobImportUrl,
    JobUpdate,
    JobSummary,
    JobSkillItem,
    JobDetail,
    JobProcessingStatus,
    JobComparisonItem,
)

from .resume import (
    ParsedResume,
    ContactInfo,
    ExperienceItem,
    EducationItem,
    CertificationItem,
    ProjectItem,
    ResumeUploadRequest,
    ResumeUpdate,
    ResumeSummary,
    ResumeDetail,
    ResumeUploadResponse,
    ResumeProcessingStatus,
    BulletPoint,
)

from .project import (
    ProjectCreate,
    ProjectUpdate,
    GitHubSyncRequest,
    ProjectSummary,
    ProjectDetail,
    GitHubSyncResponse,
    GitHubRepoPreview,
)

from .skill import (
    SkillCreate,
    SkillUpdate,
    UserSkillUpdate,
    SkillSummary,
    SkillDetail,
    UserSkillResponse,
    UserSkillDetail,
    SkillCategory,
    SkillSearchResult,
)

from .analysis import (
    AnalysisCreate,
    AnalysisQuestion,
    RadarScores,
    EvidenceItem,
    SkillTableRow,
    LearningResource,
    GapRoadmapItem,
    BonusSkillItem,
    ScoreBreakdown,
    AnalysisJsonDetail,
    AnalysisSummary,
    AnalysisResponse,
    AnalysisProcessingStatus,
    QuestionAnswer,
    AnalysisComparison,
    FrontendAnalysisPayload,
)

__all__ = [
    # Base
    "BaseSchema",
    "PaginationParams",
    "PaginatedResponse",
    "ErrorResponse",
    "SuccessResponse",
    
    # User
    "UserCreate",
    "UserUpdate",
    "UserLogin",
    "GitHubConnectRequest",
    "GitHubCallbackRequest",
    "UserResponse",
    "UserPublicProfile",
    "GitHubConnectResponse",
    "GitHubConnectionStatus",
    "AuthTokenResponse",
    "UserStats",
    
    # Job
    "JobCreate",
    "JobImportUrl",
    "JobUpdate",
    "JobSummary",
    "JobSkillItem",
    "JobDetail",
    "JobProcessingStatus",
    "JobComparisonItem",
    
    # Resume
    "ParsedResume",
    "ContactInfo",
    "ExperienceItem",
    "EducationItem",
    "CertificationItem",
    "ProjectItem",
    "ResumeUploadRequest",
    "ResumeUpdate",
    "ResumeSummary",
    "ResumeDetail",
    "ResumeUploadResponse",
    "ResumeProcessingStatus",
    "BulletPoint",
    
    # Project
    "ProjectCreate",
    "ProjectUpdate",
    "GitHubSyncRequest",
    "ProjectSummary",
    "ProjectDetail",
    "GitHubSyncResponse",
    "GitHubRepoPreview",
    
    # Skill
    "SkillCreate",
    "SkillUpdate",
    "UserSkillUpdate",
    "SkillSummary",
    "SkillDetail",
    "UserSkillResponse",
    "UserSkillDetail",
    "SkillCategory",
    "SkillSearchResult",
    
    # Analysis
    "AnalysisCreate",
    "AnalysisQuestion",
    "RadarScores",
    "EvidenceItem",
    "SkillTableRow",
    "LearningResource",
    "GapRoadmapItem",
    "BonusSkillItem",
    "ScoreBreakdown",
    "AnalysisJsonDetail",
    "AnalysisSummary",
    "AnalysisResponse",
    "AnalysisProcessingStatus",
    "QuestionAnswer",
    "AnalysisComparison",
    "FrontendAnalysisPayload",
]