"""
Recommendations module for Tinder API
Handles getting user recommendations for swiping.
"""

from typing import Any, Dict, List

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


def get_recommendations() -> List[Dict[str, Any]]:
    """
    Get user recommendations for swiping

    Returns:
        List of user profiles to swipe on
    """
    response = _make_request("GET", "/user/recs")
    return response.get("results", [])


def get_recommendations_v2() -> List[Dict[str, Any]]:
    """
    Get user recommendations using v2 API (more consistent with location changes)

    Returns:
        List of user profiles to swipe on
    """
    response = _make_request("GET", "/v2/recs/core?locale=en-US")
    return response.get("results", [])
