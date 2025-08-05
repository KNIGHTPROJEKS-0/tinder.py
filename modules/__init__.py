"""
Tinder API Modules Package
"""

from .api import (TinderAPIError, dislike, get_match_info, get_matches,
                  get_meta, get_meta_v2, get_profile, get_recommendations,
                  get_recommendations_v2, get_updates, get_user_info, like,
                  report_user, reset_location, send_message, set_location,
                  superlike, unmatch, update_profile)
from .api_modular import TinderAPIError as ModularTinderAPIError
from .api_modular import dislike as modular_dislike
from .api_modular import get_recommendations as modular_get_recommendations
from .api_modular import like as modular_like
from .api_modular import reset_location as modular_reset_location
from .api_modular import set_location as modular_set_location
from .api_modular import superlike as modular_superlike

__all__ = [
    # Main API
    "TinderAPIError",
    "get_recommendations",
    "get_recommendations_v2",
    "like",
    "dislike",
    "superlike",
    "get_matches",
    "get_match_info",
    "send_message",
    "unmatch",
    "set_location",
    "reset_location",
    "get_profile",
    "update_profile",
    "get_user_info",
    "report_user",
    "get_updates",
    "get_meta",
    "get_meta_v2",
    # Modular API
    "ModularTinderAPIError",
    "modular_get_recommendations",
    "modular_like",
    "modular_dislike",
    "modular_superlike",
    "modular_set_location",
    "modular_reset_location",
]
