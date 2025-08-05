"""
Tinder API Client
Clean implementation of Tinder API endpoints using environment-based
authentication.
"""

import logging
import os
import time
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


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


def _get_auth_token() -> str:
    """Get authentication token from environment variable"""
    token = os.getenv("TINDER_AUTH_TOKEN")
    if not token:
        raise TinderAPIError("TINDER_AUTH_TOKEN not found in environment variables")
    return token


def _get_headers() -> Dict[str, str]:
    """Get headers with authentication token"""
    headers = DEFAULT_HEADERS.copy()
    headers["X-Auth-Token"] = _get_auth_token()
    return headers


def _get_json_headers() -> Dict[str, str]:
    """Get headers with authentication token and JSON content type"""
    headers = _get_headers()
    headers["content-type"] = "application/json"
    return headers


def _make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    json_data: Optional[Dict] = None,
    max_retries: int = 3,
) -> Dict[str, Any]:
    """
    Make HTTP request to Tinder API with retry logic

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without host)
        data: Form data for POST requests
        json_data: JSON data for POST requests
        max_retries: Maximum number of retry attempts

    Returns:
        API response as dictionary

    Raises:
        TinderAPIError: If request fails after all retries
    """
    url = f"{API_HOST}{endpoint}"
    headers = _get_json_headers() if json_data else _get_headers()

    for attempt in range(max_retries + 1):
        try:
            logger.debug(f"Making {method} request to {endpoint} (attempt {attempt + 1})")

            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                if json_data:
                    response = requests.post(url, headers=headers, json=json_data, timeout=30)
                else:
                    response = requests.post(url, headers=headers, data=data, timeout=30)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=json_data, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise TinderAPIError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            logger.debug(f"Request successful: {response.status_code}")
            return response.json()

        except requests.exceptions.Timeout as e:
            logger.warning(f"Request timeout (attempt {attempt + 1}): {e}")
            if attempt == max_retries:
                raise TinderAPIError(f"Request timeout after {max_retries + 1} attempts")
            time.sleep(2**attempt)  # Exponential backoff

        except requests.exceptions.HTTPError as e:
            if e.response.status_code >= 500 and attempt < max_retries:
                logger.warning(
                    f"Server error {e.response.status_code} (attempt {attempt + 1}): {e}"
                )
                time.sleep(2**attempt)  # Exponential backoff
                continue
            else:
                logger.error(f"HTTP error {e.response.status_code}: {e}")
                raise TinderAPIError(f"HTTP error {e.response.status_code}: {str(e)}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            if attempt == max_retries:
                raise TinderAPIError(
                    f"API request failed after {max_retries + 1} attempts: {str(e)}"
                )
            time.sleep(2**attempt)  # Exponential backoff


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


def get_matches(limit: int = 60) -> List[Dict[str, Any]]:
    """
    Get user's matches

    Args:
        limit: Number of matches to retrieve (1-100)

    Returns:
        List of matches
    """
    response = _make_request("GET", f"/v2/matches?count={limit}")
    return response.get("data", {}).get("matches", [])


def get_match_info(match_id: str) -> Dict[str, Any]:
    """
    Get information about a specific match

    Args:
        match_id: Match ID

    Returns:
        Match information
    """
    return _make_request("GET", f"/matches/{match_id}")


def send_message(match_id: str, message: str) -> Dict[str, Any]:
    """
    Send a message to a match

    Args:
        match_id: Match ID
        message: Message text

    Returns:
        API response
    """
    return _make_request("POST", f"/user/matches/{match_id}", json_data={"message": message})


def unmatch(match_id: str) -> Dict[str, Any]:
    """
    Unmatch with a user

    Args:
        match_id: Match ID

    Returns:
        API response
    """
    return _make_request("DELETE", f"/user/matches/{match_id}")


def set_location(lat: float, lon: float) -> Dict[str, Any]:
    """
    Update user's location (requires Tinder Plus/Passport)

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        API response
    """
    return _make_request("POST", "/passport/user/travel", json_data={"lat": lat, "lon": lon})


def reset_location() -> Dict[str, Any]:
    """
    Reset location to real location

    Returns:
        API response
    """
    return _make_request("POST", "/passport/user/reset")


def get_profile() -> Dict[str, Any]:
    """
    Get user's own profile data

    Returns:
        Profile information
    """
    return _make_request("GET", "/profile")


def update_profile(**kwargs) -> Dict[str, Any]:
    """
    Update profile preferences

    Args:
        **kwargs: Profile parameters (age_filter_min, age_filter_max,
                 gender, distance_filter, etc.)

    Returns:
        API response
    """
    return _make_request("POST", "/profile", json_data=kwargs)


def get_user_info(user_id: str) -> Dict[str, Any]:
    """
    Get information about a specific user

    Args:
        user_id: Tinder user ID

    Returns:
        User information
    """
    return _make_request("GET", f"/user/{user_id}")


def report_user(user_id: str, cause: int, explanation: str = "") -> Dict[str, Any]:
    """
    Report a user

    Args:
        user_id: Tinder user ID
        cause: Report cause (0: Other, 1: Spam, 4: Inappropriate Photos)
        explanation: Explanation for the report

    Returns:
        API response
    """
    return _make_request(
        "POST", f"/report/{user_id}", json_data={"cause": cause, "text": explanation}
    )


def get_updates(last_activity_date: str = "") -> Dict[str, Any]:
    """
    Get updates since the given activity date

    Args:
        last_activity_date: ISO timestamp (e.g., "2017-07-09T10:28:13.392Z")

    Returns:
        Updates data
    """
    return _make_request("POST", "/updates", json_data={"last_activity_date": last_activity_date})


def get_meta() -> Dict[str, Any]:
    """
    Get user's meta data (swipes, people seen, etc.)

    Returns:
        Meta data
    """
    return _make_request("GET", "/meta")


def get_meta_v2() -> Dict[str, Any]:
    """
    Get user's meta data from v2 API (includes top picks info)

    Returns:
        Meta data
    """
    return _make_request("GET", "/v2/meta")
