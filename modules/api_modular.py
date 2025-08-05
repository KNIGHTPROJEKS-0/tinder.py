"""
Modular Tinder API Client
Unified interface that combines functionality from separate modules.
"""

# Import core functionality from modules
from .auth import TinderAPIError, get_auth_token
from .location import reset_location, set_location
from .recs import get_recommendations, get_recommendations_v2
from .swipe import dislike, like, superlike

# Re-export for easy access
__all__ = [
    "TinderAPIError",
    "get_auth_token",
    "get_recommendations",
    "get_recommendations_v2",
    "like",
    "dislike",
    "superlike",
    "set_location",
    "reset_location",
]
