"""Tools for the chat assistant agent.

Pure data-fetching tools — they call the backend API and return
formatted strings for the chat agent to read and reason about.
"""

import json
import logging

from langchain_core.tools import tool

from src.integrations.backend_client import (
    fetch_all_jobs,
    fetch_job_by_id,
    fetch_all_freelancers,
    fetch_freelancer_by_id,
    fetch_all_contractors,
    fetch_contractor_by_id,
)

logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:3000"


# ==================== Formatting Helpers ====================


def _format_job_list(jobs: list[dict]) -> str:
    """Format jobs list data into a human-readable string with summary and links."""
    # Filter out non-dict items for robustness
    valid_jobs = [job for job in jobs if isinstance(job, dict)]
    total = len(valid_jobs)

    lines = [f"Summary: Total {total} jobs available on the platform.\n"]

    for i, job in enumerate(valid_jobs, 1):
        job_id = job.get("id", "")
        title = job.get("title", "N/A")
        category = job.get("category", "N/A")
        status = job.get("status", "N/A")
        budget_min = job.get("budgetMin", 0)
        budget_max = job.get("budgetMax", 0)
        skills = ", ".join(job.get("skills", []))
        link = f"{BASE_URL}/projects/{job_id}"

        lines.append(
            f"{i}. {title}\n"
            f"   - ID: {job_id}\n"
            f"   - Category: {category}\n"
            f"   - Skills: {skills}\n"
            f"   - Budget: {budget_min:,} - {budget_max:,} VND\n"
            f"   - Status: {status}\n"
            f"   - Link: {link}"
        )

    return "\n".join(lines)


def _format_freelancer_list(freelancers: list[dict]) -> str:
    """Format freelancers list data into a human-readable string with summary and links."""
    # Filter out non-dict items for robustness
    valid_freelancers = [fl for fl in freelancers if isinstance(fl, dict)]
    total = len(valid_freelancers)

    lines = [f"Summary: Total {total} freelancers available on the platform.\n"]

    for i, fl in enumerate(valid_freelancers, 1):
        fl_id = fl.get("id", "")
        full_name = fl.get("fullName", "N/A")
        role = fl.get("role", "N/A")
        rating_avg = fl.get("ratingAvg", 0)
        rating_count = fl.get("ratingCount", 0)
        status = fl.get("status", "N/A")
        link = f"{BASE_URL}/freelancers/{fl_id}"

        lines.append(
            f"{i}. {full_name}\n"
            f"   - ID: {fl_id}\n"
            f"   - Role: {role}\n"
            f"   - Rating: {rating_avg} ({rating_count} reviews)\n"
            f"   - Status: {status}\n"
            f"   - Link: {link}"
        )

    return "\n".join(lines)


def _format_contractor_list(contractors: list[dict]) -> str:
    """Format contractors list data into a human-readable string with summary and links."""
    # Filter out non-dict items for robustness
    valid_contractors = [ct for ct in contractors if isinstance(ct, dict)]
    total = len(valid_contractors)

    lines = [f"Summary: Total {total} contractors available on the platform.\n"]

    for i, ct in enumerate(valid_contractors, 1):
        ct_id = ct.get("id", "")
        full_name = ct.get("fullName", "N/A")
        role = ct.get("role", "N/A")
        rating_avg = ct.get("ratingAvg", 0)
        rating_count = ct.get("ratingCount", 0)
        status = ct.get("status", "N/A")
        link = f"{BASE_URL}/freelancers/{ct_id}"

        lines.append(
            f"{i}. {full_name}\n"
            f"   - ID: {ct_id}\n"
            f"   - Role: {role}\n"
            f"   - Rating: {rating_avg} ({rating_count} reviews)\n"
            f"   - Status: {status}\n"
            f"   - Link: {link}"
        )

    return "\n".join(lines)


# ==================== Job Tools ====================


@tool(
    description=(
        "Get all available jobs/projects on the platform. "
        "Use when a freelancer wants to browse jobs, find work, "
        "or needs job recommendations."
    )
)
async def get_all_jobs() -> str:
    """Fetch all open jobs and return as a formatted string with summary and links."""
    jobs = await fetch_all_jobs()
    if not jobs:
        return "No jobs available at the moment or backend is unavailable."


    return _format_job_list(jobs)


@tool(
    description=(
        "Get detailed information about a specific job/project by its ID. "
        "Use when a user asks about a particular job or you need full job details. "
        "Prefer using IDs from conversation context or previous tool results."
    )
)
async def get_job_details(job_id: str) -> str:
    """Fetch a single job by ID and return its details as JSON object."""
    job = await fetch_job_by_id(job_id)
    if not job:
        return f"Job with ID '{job_id}' not found."

    # Add link to the job detail object
    if isinstance(job, dict):
        job["link"] = f"{BASE_URL}/projects/{job.get('id', job_id)}"


    return json.dumps(job, indent=2, default=str)


# ==================== Freelancer Tools ====================


@tool(
    description=(
        "Get all available freelancers on the platform (users with role=freelancer). "
        "Use when a contractor/client wants to find freelancers, "
        "browse candidates, or needs freelancer recommendations."
    )
)
async def get_all_freelancers() -> str:
    """Fetch all active freelancers and return as a formatted string with summary and links."""
    freelancers = await fetch_all_freelancers()
    if not freelancers:
        return "No freelancers available at the moment or backend is unavailable."


    return _format_freelancer_list(freelancers)


@tool(
    description=(
        "Get detailed information about a specific freelancer by their ID. "
        "Use when a user asks about a particular freelancer or you need full profile details. "
        "Prefer using IDs from conversation context or previous tool results."
    )
)
async def get_freelancer_details(freelancer_id: str) -> str:
    """Fetch a single freelancer by ID and return their profile as JSON object."""
    freelancer = await fetch_freelancer_by_id(freelancer_id)
    if not freelancer:
        return f"Freelancer with ID '{freelancer_id}' not found."

    # Add link to the freelancer detail object
    if isinstance(freelancer, dict):
        freelancer["link"] = f"{BASE_URL}/freelancers/{freelancer.get('id', freelancer_id)}"


    return json.dumps(freelancer, indent=2, default=str)


# ==================== Contractor Tools ====================


@tool(
    description=(
        "Get all available contractors/clients on the platform (users with role=contractor). "
        "Use when a freelancer wants to find clients, "
        "or needs to browse who is hiring."
    )
)
async def get_all_contractors() -> str:
    """Fetch all active contractors and return as a formatted string with summary and links."""
    contractors = await fetch_all_contractors()
    if not contractors:
        return "No contractors available at the moment or backend is unavailable."

    return _format_contractor_list(contractors)


@tool(
    description=(
        "Get detailed information about a specific contractor/client by their ID. "
        "Use when a user asks about a particular contractor or you need full profile details. "
        "Prefer using IDs from conversation context or previous tool results."
    )
)
async def get_contractor_details(contractor_id: str) -> str:
    """Fetch a single contractor by ID and return their profile as JSON object."""
    contractor = await fetch_contractor_by_id(contractor_id)
    if not contractor:
        return f"Contractor with ID '{contractor_id}' not found."

    # Add link to the contractor detail object
    if isinstance(contractor, dict):
        contractor["link"] = f"{BASE_URL}/freelancers/{contractor.get('id', contractor_id)}"

    return json.dumps(contractor, indent=2, default=str)


# All tools available to the chat agent
ALL_TOOLS = [
    get_all_jobs,
    get_job_details,
    get_all_freelancers,
    get_freelancer_details,
    get_all_contractors,
    get_contractor_details,
]

TOOL_MAP = {t.name: t for t in ALL_TOOLS}
