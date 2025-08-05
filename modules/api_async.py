"""
Async Tinder API Client
Clean async implementation of Tinder API endpoints using httpx.
"""

import os
from typing import Any, Dict, List, Optional

import httpx
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


class AsyncTinderAPI:
    """Async Tinder API client"""

    def __init__(self, auth_token: Optional[str] = None):
        """
        Initialize the async Tinder API client

        Args:
            auth_token: Optional auth token. If not provided, will load from env
        """
        self.auth_token = auth_token or self._get_auth_token()
        self.client = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.client = httpx.AsyncClient(headers=self._get_headers(), timeout=30.0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.client:
            await self.client.aclose()

    def _get_auth_token(self) -> str:
        """Get authentication token from environment variable"""
        token = os.getenv("TINDER_AUTH_TOKEN")
        if not token:
            raise TinderAPIError("TINDER_AUTH_TOKEN not found in environment variables")
        return token

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token"""
        headers = DEFAULT_HEADERS.copy()
        headers["X-Auth-Token"] = self.auth_token
        return headers

    def _get_json_headers(self) -> Dict[str, str]:
        """Get headers with authentication token and JSON content type"""
        headers = self._get_headers()
        headers["content-type"] = "application/json"
        return headers

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Make async HTTP request to Tinder API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without host)
            data: Form data for POST requests
            json_data: JSON data for POST requests

        Returns:
            API response as dictionary

        Raises:
            TinderAPIError: If request fails
        """
        url = f"{API_HOST}{endpoint}"
        headers = self._get_json_headers() if json_data else self._get_headers()

        try:
            if method.upper() == "GET":
                response = await self.client.get(url, headers=headers)
            elif method.upper() == "POST":
                if json_data:
                    response = await self.client.post(url, headers=headers, json=json_data)
                else:
                    response = await self.client.post(url, headers=headers, data=data)
            elif method.upper() == "PUT":
                response = await self.client.put(url, headers=headers, json=json_data)
            elif method.upper() == "DELETE":
                response = await self.client.delete(url, headers=headers)
            else:
                raise TinderAPIError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except httpx.RequestError as e:
            raise TinderAPIError(f"API request failed: {str(e)}")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def get_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get user recommendations for swiping

        Returns:
            List of user profiles to swipe on
        """
        response = await self._make_request("GET", "/user/recs")
        return response.get("results", [])

    async def get_recommendations_v2(self) -> List[Dict[str, Any]]:
        """
        Get user recommendations using v2 API

        Returns:
            List of user profiles to swipe on
        """
        response = await self._make_request("GET", "/v2/recs/core?locale=en-US")
        return response.get("results", [])

    async def like(self, user_id: str) -> Dict[str, Any]:
        """
        Like a user (swipe right)

        Args:
            user_id: Tinder user ID

        Returns:
            API response
        """
        return await self._make_request("GET", f"/like/{user_id}")

    async def dislike(self, user_id: str) -> Dict[str, Any]:
        """
        Dislike a user (swipe left)

        Args:
            user_id: Tinder user ID

        Returns:
            API response
        """
        return await self._make_request("GET", f"/pass/{user_id}")

    async def superlike(self, user_id: str) -> Dict[str, Any]:
        """
        Super like a user (swipe up)

        Args:
            user_id: Tinder user ID

        Returns:
            API response
        """
        return await self._make_request("POST", f"/like/{user_id}/super")

    async def get_matches(self, limit: int = 60) -> List[Dict[str, Any]]:
        """
        Get user's matches

        Args:
            limit: Number of matches to retrieve (1-100)

        Returns:
            List of matches
        """
        response = await self._make_request("GET", f"/v2/matches?count={limit}")
        return response.get("data", {}).get("matches", [])

    async def get_match_info(self, match_id: str) -> Dict[str, Any]:
        """
        Get information about a specific match

        Args:
            match_id: Match ID

        Returns:
            Match information
        """
        return await self._make_request("GET", f"/matches/{match_id}")

    async def send_message(self, match_id: str, message: str) -> Dict[str, Any]:
        """
        Send a message to a match

        Args:
            match_id: Match ID
            message: Message text

        Returns:
            API response
        """
        return await self._make_request(
            "POST", f"/user/matches/{match_id}", json_data={"message": message}
        )

    async def unmatch(self, match_id: str) -> Dict[str, Any]:
        """
        Unmatch with a user

        Args:
            match_id: Match ID

        Returns:
            API response
        """
        return await self._make_request("DELETE", f"/user/matches/{match_id}")

    async def set_location(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Update user's location (requires Tinder Plus/Passport)

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            API response
        """
        return await self._make_request(
            "POST", "/passport/user/travel", json_data={"lat": lat, "lon": lon}
        )

    async def reset_location(self) -> Dict[str, Any]:
        """
        Reset location to real location

        Returns:
            API response
        """
        return await self._make_request("POST", "/passport/user/reset")

    async def get_profile(self) -> Dict[str, Any]:
        """
        Get user's own profile data

        Returns:
            Profile information
        """
        return await self._make_request("GET", "/profile")

    async def update_profile(self, **kwargs) -> Dict[str, Any]:
        """
        Update profile preferences

        Args:
            **kwargs: Profile parameters

        Returns:
            API response
        """
        return await self._make_request("POST", "/profile", json_data=kwargs)

    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """
        Get information about a specific user

        Args:
            user_id: Tinder user ID

        Returns:
            User information
        """
        return await self._make_request("GET", f"/user/{user_id}")

    async def report_user(self, user_id: str, cause: int, explanation: str = "") -> Dict[str, Any]:
        """
        Report a user

        Args:
            user_id: Tinder user ID
            cause: Report cause (0: Other, 1: Spam, 4: Inappropriate Photos)
            explanation: Explanation for the report

        Returns:
            API response
        """
        return await self._make_request(
            "POST", f"/report/{user_id}", json_data={"cause": cause, "text": explanation}
        )

    async def get_updates(self, last_activity_date: str = "") -> Dict[str, Any]:
        """
        Get updates since the given activity date

        Args:
            last_activity_date: ISO timestamp

        Returns:
            Updates data
        """
        return await self._make_request(
            "POST", "/updates", json_data={"last_activity_date": last_activity_date}
        )

    async def get_meta(self) -> Dict[str, Any]:
        """
        Get user's meta data

        Returns:
            Meta data
        """
        return await self._make_request("GET", "/meta")

    async def get_meta_v2(self) -> Dict[str, Any]:
        """
        Get user's meta data from v2 API

        Returns:
            Meta data
        """
        return await self._make_request("GET", "/v2/meta")


# Convenience functions for backward compatibility
async def get_recommendations() -> List[Dict[str, Any]]:
    """Get user recommendations (async)"""
    async with AsyncTinderAPI() as api:
        return await api.get_recommendations()


async def like(user_id: str) -> Dict[str, Any]:
    """Like a user (async)"""
    async with AsyncTinderAPI() as api:
        return await api.like(user_id)


async def dislike(user_id: str) -> Dict[str, Any]:
    """Dislike a user (async)"""
    async with AsyncTinderAPI() as api:
        return await api.dislike(user_id)


async def get_matches(limit: int = 60) -> List[Dict[str, Any]]:
    """Get matches (async)"""
    async with AsyncTinderAPI() as api:
        return await api.get_matches(limit)


async def set_location(lat: float, lon: float) -> Dict[str, Any]:
    """Set location (async)"""
    async with AsyncTinderAPI() as api:
        return await api.set_location(lat, lon)
