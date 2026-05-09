"""MongoDB database connection singleton.

Note: The AI service no longer uses direct MongoDB access.
All data operations go through the Node.js backend API.
This module is kept for potential future direct DB needs.
"""

import logging
from pymongo import MongoClient
from pymongo.database import Database
from src.core.config import settings

logger = logging.getLogger(__name__)

_client: MongoClient | None = None
_database: Database | None = None


def get_client() -> MongoClient:
    """Get or create the MongoDB client singleton."""
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGODB_URI)
        logger.info("MongoDB client created")
    return _client


def get_database() -> Database:
    """Get the application database."""
    global _database
    if _database is None:
        client = get_client()
        _database = client[settings.MONGODB_DB_NAME]
        logger.info(f"Connected to database: {settings.MONGODB_DB_NAME}")
    return _database


def init_database() -> None:
    """Initialize database connection (no indexes needed currently)."""
    logger.info("Database module initialized (no direct collections used)")


def close_database() -> None:
    """Close the MongoDB connection."""
    global _client, _database
    if _client is not None:
        _client.close()
        _client = None
        _database = None
        logger.info("MongoDB connection closed")
