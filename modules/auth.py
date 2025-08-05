"""
Authentication module for Tinder API
Handles token management and authentication headers.
"""

import os
from typing import Dict

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_HOST = "https://api.gotinder.com"
DEFAULT_HEADERS = {
    "app_version": "6.9.4",
    "platform": "ios",
    "User-agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
    "Accept": "application/json",
}


class TinderAPIError(Exception):
    """Custom exception for Tinder API errors"""

    pass


def get_auth_token() -> str:
    """Get authentication token from environment variable"""
    token = os.getenv("TINDER_AUTH_TOKEN")
    if not token:
        raise TinderAPIError("TINDER_AUTH_TOKEN not found in environment variables")
    return token


def get_headers() -> Dict[str, str]:
    """Get headers with authentication token"""
    headers = DEFAULT_HEADERS.copy()
    headers["X-Auth-Token"] = get_auth_token()
    return headers


def get_json_headers() -> Dict[str, str]:
    """Get headers with authentication token and JSON content type"""
    headers = get_headers()
    headers["content-type"] = "application/json"
    return headers
