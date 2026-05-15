"""HTTP client for the Node.js backend API.

Fetches real data from the backend API endpoints.
"""

import httpx
import logging
from typing import Optional

from src.core.config import settings

logger = logging.getLogger(__name__)

BASE_URL = f"{settings.BACKEND_API_URL}/internal/ai"

# Timeout: 10 seconds connect, 30 seconds read
TIMEOUT = httpx.Timeout(10.0, read=30.0)


async def fetch_all_jobs() -> Optional[list[dict]]:
    """Fetch all open jobs from the backend API.

    Returns:
        List of job dicts in AI format, or None if backend unavailable.
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/jobs")
            response.raise_for_status()
            data = response.json()
            return data.get("jobs", [])
    except Exception as e:
        logger.warning(f"Failed to fetch jobs from backend: {e}")
        return []


async def fetch_job_by_id(job_id: str) -> Optional[dict]:
    """Fetch a single job by ID from the backend API.

    Args:
        job_id: The project/job ID (MongoDB ObjectId string).

    Returns:
        Job dict in AI format, or None if not found/unavailable.
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/jobs/{job_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.warning(f"Failed to fetch job {job_id} from backend: {e}")
        return None

async def fetch_all_freelancers() -> Optional[list[dict]]:
    """Fetch all active freelancers from the backend API.

    Returns:
        List of freelancer dicts in AI format, or None if backend unavailable.
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/freelancers")
            response.raise_for_status()
            data = response.json()
            return data.get("freelancers", [])
    except Exception as e:
        logger.warning(f"Failed to fetch freelancers from backend: {e}")
        return []


async def fetch_freelancer_by_id(freelancer_id: str) -> Optional[dict]:
    """Fetch a single freelancer by ID from the backend API.

    Args:
        freelancer_id: The user ID (MongoDB ObjectId string).

    Returns:
        Freelancer dict in AI format, or None if not found/unavailable.
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/freelancers/{freelancer_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.warning(f"Failed to fetch freelancer {freelancer_id} from backend: {e}")
        return None

async def fetch_all_contractors() -> Optional[list[dict]]:
    """Fetch all active contractors from the backend API.

    Returns:
        List of contractor dicts in AI format, or None if backend unavailable.
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/contractors")
            response.raise_for_status()
            data = response.json()
            return data.get("contractors", [])
    except Exception as e:
        logger.warning(f"Failed to fetch contractors from backend: {e}")
        return []


async def fetch_contractor_by_id(contractor_id: str) -> Optional[dict]:
    """Fetch a single contractor by ID from the backend API.

    Args:
        contractor_id: The user ID (MongoDB ObjectId string).

    Returns:
        Contractor dict in AI format, or None if not found/unavailable.
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{BASE_URL}/contractors/{contractor_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.warning(f"Failed to fetch contractor {contractor_id} from backend: {e}")
        return None

async def fetch_messages(group_id: str, limit: int = 10) -> Optional[list[dict]]:
    """Fetch the last N messages of a group for conversation context.

    Args:
        group_id: The chat group ObjectId string.
        limit: Number of recent messages to fetch (default 10).

    Returns:
        List of message dicts with role/content, or None if unavailable.
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(
                f"{BASE_URL}/groups/{group_id}/messages", params={"limit": limit}
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            return data.get("messages", [])
    except Exception as e:
        logger.warning(f"Failed to fetch messages for group {group_id}: {e}")
        return None


async def post_ai_message(group_id: str, content: str) -> Optional[dict]:
    """Save an AI-generated message into a group via the backend API.

    Args:
        group_id: The chat group ObjectId string.
        content: The AI response text.

    Returns:
        Created message dict, or None if failed.
    """
    url = f"{BASE_URL}/groups/{group_id}/messages"
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(url, json={"content": content})
            response.raise_for_status()
            data = response.json()
            return data.get("data")
    except Exception as e:
        logger.warning(f"Failed to post AI message to group {group_id}: {e}")
        return None
