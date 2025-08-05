"""
Location module for Tinder API
Handles location updates and travel features.
"""

from typing import Any, Dict

import requests

from .auth import API_HOST, TinderAPIError, get_headers, get_json_headers


def _make_request(method: str, endpoint: str, json_data: Dict = None) -> Dict[str, Any]:
    """Make HTTP request to Tinder API"""
    url = f"{API_HOST}{endpoint}"
    headers = get_json_headers() if json_data else get_headers()

    try:
        if method.upper() == "POST":
            response = requests.post(url, headers=headers, json=json_data)
        else:
            raise TinderAPIError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise TinderAPIError(f"API request failed: {str(e)}")


def set_location(lat: float, lon: float) -> Dict[str, Any]:
    """
    Update user's location (requires Tinder Plus/Passport)

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        API response
    """
    return _make_request("POST", "/passport/user/travel", {"lat": lat, "lon": lon})


def reset_location() -> Dict[str, Any]:
    """
    Reset location to real location

    Returns:
        API response
    """
    return _make_request("POST", "/passport/user/reset")
