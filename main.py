"""
Tinder API Usage Example
Demonstrates how to use the Tinder API to like users with specific interests.
"""

import os
import time
from typing import Optional

from modules.api import TinderAPIError, get_recommendations, like


def check_environment() -> bool:
    """Check if required environment variables are set"""
    if not os.getenv('TINDER_AUTH_TOKEN'):
        print("[ERROR] TINDER_AUTH_TOKEN not found in environment variables")
        print("[INFO] Please create a .env file with your Tinder auth token:")
        print("       TINDER_AUTH_TOKEN=your_token_here")
        return False
    return True


def main() -> None:
    """Main function that demonstrates Tinder API usage"""
    print("[INFO] Starting Tinder API automation...")
    
    # Check environment setup
    if not check_environment():
        return

    try:
        # Get user recommendations
        print("[INFO] Fetching user recommendations...")
        users = get_recommendations()

        if not users:
            print("[INFO] No recommendations available at the moment.")
            return

        print(f"[INFO] Found {len(users)} users to review")

        # Process each user
        for i, user in enumerate(users, 1):
            user_id: Optional[str] = user.get("_id")
            name = user.get("name", "Unknown")
            bio = user.get("bio", "").lower()

            print(f"\n[{i}/{len(users)}] Reviewing {name}...")

            # Check if user has 'music' in their bio
            if "music" in bio and user_id:
                print(f"  ✓ {name} likes music! Swiping right...")
                try:
                    result = like(user_id)
                    if result.get("match"):
                        print(f"  🎉 It's a match with {name}!")
                    else:
                        print(f"  ✓ Liked {name}")
                except TinderAPIError as e:
                    print(f"  ✗ Error liking {name}: {e}")
            else:
                print(f"  - {name} doesn't mention music in bio")

            # Add a small delay to avoid rate limiting
            time.sleep(1)

        print(f"\n[INFO] Completed review of {len(users)} users")

    except TinderAPIError as e:
        print(f"[ERROR] API Error: {e}")
        print("[INFO] This might be due to:")
        print("       - Invalid auth token")
        print("       - Rate limiting")
        print("       - Network issues")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")


if __name__ == "__main__":
    main()
