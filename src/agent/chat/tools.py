"""Tools for the chat assistant agent.

Pure data-fetching tools — they call the backend API and return
JSON strings for the chat agent to read and reason about.
"""

import json
import logging

from langchain_core.tools import tool

from src.integrations.backend_client import (
    fetch_all_jobs, fetch_job_by_id,
    fetch_all_freelancers, fetch_freelancer_by_id
)

logger = logging.getLogger(__name__)


# ==================== Job Tools ====================

@tool(
    description=(
        "Get all available jobs/projects on the platform. "
        "Use when a freelancer wants to browse jobs, find work, "
        "or needs job recommendations."
    )
)
async def get_all_jobs() -> str:
    """Fetch all open jobs and return as JSON string."""
    jobs = await fetch_all_jobs()
    if not jobs:
        return "No jobs available at the moment or backend is unavailable."
    return json.dumps(jobs, indent=2, default=str)


@tool(
    description=(
        "Get detailed information about a specific job/project by its ID. "
        "Use when a user asks about a particular job or you need full job details. "
        "Prefer using IDs from conversation context or previous tool results."
    )
)
async def get_job_details(job_id: str) -> str:
    """Fetch a single job by ID and return its details as JSON string."""
    job = await fetch_job_by_id(job_id)
    if not job:
        return f"Job with ID '{job_id}' not found."
    return json.dumps(job, indent=2, default=str)


# ==================== Freelancer Tools ====================

@tool(
    description=(
        "Get all available freelancers on the platform. "
        "Use when a contractor/client wants to find freelancers, "
        "browse candidates, or needs freelancer recommendations."
    )
)
async def get_all_freelancers() -> str:
    """Fetch all active freelancers and return as JSON string."""
    freelancers = await fetch_all_freelancers()
    if not freelancers:
        return "No freelancers available at the moment or backend is unavailable."
    return json.dumps(freelancers, indent=2, default=str)


@tool(
    description=(
        "Get detailed information about a specific freelancer by their ID. "
        "Use when a user asks about a particular freelancer or you need full profile details. "
        "Prefer using IDs from conversation context or previous tool results."
    )
)
async def get_freelancer_details(freelancer_id: str) -> str:
    """Fetch a single freelancer by ID and return their profile as JSON string."""
    freelancer = await fetch_freelancer_by_id(freelancer_id)
    if not freelancer:
        return f"Freelancer with ID '{freelancer_id}' not found."
    return json.dumps(freelancer, indent=2, default=str)


# All tools available to the chat agent
ALL_TOOLS = [
    get_all_jobs,
    get_job_details,
    get_all_freelancers,
    get_freelancer_details,
]

TOOL_MAP = {t.name: t for t in ALL_TOOLS}
