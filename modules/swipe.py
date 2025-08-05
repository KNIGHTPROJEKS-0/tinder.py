"""
Swipe module for Tinder API
Handles like, dislike, and superlike actions.
"""

from typing import Any, Dict

import requests

from .auth import API_HOST, TinderAPIError, get_headers, get_json_headers


def _make_request(method: str, endpoint: str, json_data: Dict = None) -> Dict[str, Any]:
    """Make HTTP request to Tinder API"""
    url = f"{API_HOST}{endpoint}"
    headers = get_json_headers() if json_data else get_headers()

    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=json_data)
        else:
            raise TinderAPIError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise TinderAPIError(f"API request failed: {str(e)}")


def like(user_id: str) -> Dict[str, Any]:
    """
    Like a user (swipe right)

    Args:
        user_id: Tinder user ID

    Returns:
        API response
    """
    return _make_request("GET", f"/like/{user_id}")


def dislike(user_id: str) -> Dict[str, Any]:
    """
    Dislike a user (swipe left)

    Args:
        user_id: Tinder user ID

    Returns:
        API response
    """
    return _make_request("GET", f"/pass/{user_id}")


def superlike(user_id: str) -> Dict[str, Any]:
    """
    Super like a user (swipe up)

    Args:
        user_id: Tinder user ID

    Returns:
        API response
    """
    return _make_request("POST", f"/like/{user_id}/super")
