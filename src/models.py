"""Data models for the AI platform.

Backend API returns camelCase fields. Pydantic models use Field(alias=...)
to accept camelCase input and expose snake_case attributes in Python code.
Use model_dump(by_alias=True) to serialize back to camelCase if needed.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# ==================== Backend Data Models ====================

class JobBase(BaseModel):
    """Base job model. Accepts camelCase from backend API."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    description: str
    category: str
    skills: list[str] = Field(default_factory=list)
    budget_min: float = Field(default=0, alias="budgetMin")
    budget_max: float = Field(default=0, alias="budgetMax")
    status: str = ""
    contractor_id: str = Field(default="", alias="contractorId")
    created_at: str = Field(default="", alias="createdAt")


class FreelancerBase(BaseModel):
    """Base freelancer model. Accepts camelCase from backend API."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    full_name: str = Field(default="", alias="fullName")
    description: str = ""
    role: str = ""
    rating_avg: Optional[float] = Field(default=None, alias="ratingAvg")
    rating_count: Optional[float] = Field(default=None, alias="ratingCount")
    status: str = ""


# ==================== Matching Result (used internally by tools) ====================

class MatchingResult(BaseModel):
    """Matching result with score and reason."""
    id: str
    name: str
    title: str
    match_score: float
    reason: str
    details: dict


# ==================== Chat API Models ====================

class ChatRequest(BaseModel):
    """Chat request. Uses groupId (conversationId) to identify the AI thread."""
    message: str
    group_id: str  # Conversation/group ObjectId from main chat system
    user_id: str  # Backend User ObjectId string
    user_type: str = "freelancer"  # "freelancer" or "contractor"


class ChatResponse(BaseModel):
    """Chat response."""
    message: str
    group_id: str  # Conversation/group ObjectId
    user_type: str
