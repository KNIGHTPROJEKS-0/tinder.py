"""
Example usage of the modular Tinder API
Demonstrates how to use the separated modules for different functionality.
"""

import asyncio
import time

from modules.api_async import AsyncTinderAPI
from modules.api_modular import (TinderAPIError, dislike, get_recommendations,
                                 like, reset_location, set_location)


def sync_example():
    """Synchronous example using the modular API"""
    print("=== Synchronous API Example ===")

    try:
        # Get recommendations
        print("Getting user recommendations...")
        users = get_recommendations()

        if not users:
            print("No recommendations available.")
            return

        print(f"Found {len(users)} users to review")

        # Process users
        for i, user in enumerate(users[:5], 1):  # Limit to 5 for demo
            user_id = user.get("_id")
            name = user.get("name", "Unknown")
            bio = user.get("bio", "").lower()

            print(f"\n[{i}/5] Reviewing {name}...")

            # Check for specific interests
            if any(interest in bio for interest in ["music", "travel", "photography"]):
                print(f"  ✓ {name} has interesting interests! Swiping right...")
                try:
                    result = like(user_id)
                    if result.get("match"):
                        print(f"  🎉 It's a match with {name}!")
                    else:
                        print(f"  ✓ Liked {name}")
                except TinderAPIError as e:
                    print(f"  ✗ Error liking {name}: {e}")
            else:
                print(f"  - {name} doesn't match criteria")

            time.sleep(1)  # Rate limiting

        print("\nCompleted synchronous example!")

    except TinderAPIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


async def async_example():
    """Asynchronous example using the async API"""
    print("\n=== Asynchronous API Example ===")

    try:
        async with AsyncTinderAPI() as api:
            # Get recommendations
            print("Getting user recommendations (async)...")
            users = await api.get_recommendations()

            if not users:
                print("No recommendations available.")
                return

            print(f"Found {len(users)} users to review")

            # Process users concurrently (with rate limiting)
            tasks = []
            for i, user in enumerate(users[:3], 1):  # Limit to 3 for demo
                user_id = user.get("_id")
                name = user.get("name", "Unknown")
                bio = user.get("bio", "").lower()

                print(f"\n[{i}/3] Reviewing {name}...")

                # Check for specific interests
                if "music" in bio:
                    print(f"  ✓ {name} likes music! Swiping right...")
                    # Add delay to avoid rate limiting
                    await asyncio.sleep(i * 0.5)
                    tasks.append(api.like(user_id))
                else:
                    print(f"  - {name} doesn't mention music")

            # Wait for all like operations to complete
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        print(f"  ✗ Error in like operation {i+1}: {result}")
                    elif result.get("match"):
                        print(f"  🎉 Got a match!")
                    else:
                        print(f"  ✓ Like operation {i+1} completed")

        print("\nCompleted asynchronous example!")

    except TinderAPIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def location_example():
    """Example of location-based features"""
    print("\n=== Location Example ===")

    try:
        # Note: This requires Tinder Plus/Passport
        print("Setting location to New York...")
        result = set_location(40.7128, -74.0060)  # NYC coordinates
        print(f"Location set successfully: {result}")

        # Reset to real location
        print("Resetting to real location...")
        result = reset_location()
        print(f"Location reset successfully: {result}")

    except TinderAPIError as e:
        print(f"Location API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    """Main function that runs all examples"""
    print("Tinder API Modular Example")
    print("=" * 40)

    # Run synchronous example
    sync_example()

    # Run asynchronous example
    asyncio.run(async_example())

    # Run location example
    location_example()

    print("\n" + "=" * 40)
    print("All examples completed!")


if __name__ == "__main__":
    main()
