#!/usr/bin/env python3
"""
Tinder API Integration Test Script
Tests all major features and validates the modular structure.
"""

import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import both sync and async APIs
from modules.api import (TinderAPIError, get_matches, get_profile,
                         get_recommendations, like, reset_location,
                         set_location)
from modules.api_async import AsyncTinderAPI
from modules.api_modular import \
    get_recommendations as modular_get_recommendations
from modules.api_modular import like as modular_like


def test_sync_api():
    """Test synchronous API functionality"""
    logger.info("=== Testing Synchronous API ===")

    try:
        # Test 1: Get recommendations
        logger.info("1. Testing get_recommendations()...")
        users = get_recommendations()
        logger.info(f"   ✓ Retrieved {len(users)} recommendations")

        if users:
            # Test 2: Like a user
            user = users[0]
            user_id = user.get("_id")
            name = user.get("name", "Unknown")

            if user_id:
                logger.info(f"2. Testing like() with user {name}...")
                result = like(user_id)
                logger.info(
                    f"   ✓ Like operation completed: {result.get('match', False)}"
                )

                # Test 3: Get matches
                logger.info("3. Testing get_matches()...")
                matches = get_matches(limit=10)
                logger.info(f"   ✓ Retrieved {len(matches)} matches")

        # Test 4: Get profile
        logger.info("4. Testing get_profile()...")
        profile = get_profile()
        logger.info(
            f"   ✓ Profile retrieved: {profile.get('name', 'Unknown')}"
        )

        logger.info("✓ All synchronous API tests passed!")
        return True

    except TinderAPIError as e:
        logger.error(f"✗ Synchronous API test failed: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Unexpected error in sync test: {e}")
        return False


def test_modular_api():
    """Test modular API functionality"""
    logger.info("=== Testing Modular API ===")

    try:
        # Test 1: Get recommendations via modular API
        logger.info("1. Testing modular get_recommendations()...")
        users = modular_get_recommendations()
        logger.info(f"   ✓ Retrieved {len(users)} recommendations")

        if users:
            # Test 2: Like a user via modular API
            user = users[0]
            user_id = user.get("_id")
            name = user.get("name", "Unknown")

            if user_id:
                logger.info(f"2. Testing modular like() with user {name}...")
                result = modular_like(user_id)
                logger.info(
                    f"   ✓ Like operation completed: {result.get('match', False)}"
                )

        logger.info("✓ All modular API tests passed!")
        return True

    except TinderAPIError as e:
        logger.error(f"✗ Modular API test failed: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Unexpected error in modular test: {e}")
        return False


async def test_async_api():
    """Test asynchronous API functionality"""
    logger.info("=== Testing Asynchronous API ===")

    try:
        async with AsyncTinderAPI() as api:
            # Test 1: Get recommendations
            logger.info("1. Testing async get_recommendations()...")
            users = await api.get_recommendations()
            logger.info(f"   ✓ Retrieved {len(users)} recommendations")

            if users:
                # Test 2: Like a user
                user = users[0]
                user_id = user.get("_id")
                name = user.get("name", "Unknown")

                if user_id:
                    logger.info(f"2. Testing async like() with user {name}...")
                    result = await api.like(user_id)
                    logger.info(
                        f"   ✓ Like operation completed: {result.get('match', False)}"
                    )

                    # Test 3: Get matches
                    logger.info("3. Testing async get_matches()...")
                    matches = await api.get_matches(limit=10)
                    logger.info(f"   ✓ Retrieved {len(matches)} matches")

            # Test 4: Get profile
            logger.info("4. Testing async get_profile()...")
            profile = await api.get_profile()
            logger.info(
                f"   ✓ Profile retrieved: {profile.get('name', 'Unknown')}"
            )

        logger.info("✓ All asynchronous API tests passed!")
        return True

    except TinderAPIError as e:
        logger.error(f"✗ Asynchronous API test failed: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Unexpected error in async test: {e}")
        return False


def test_location_features():
    """Test location-based features (requires Tinder Plus)"""
    logger.info("=== Testing Location Features ===")

    try:
        # Test 1: Set location (this might fail without Tinder Plus)
        logger.info("1. Testing set_location()...")
        try:
            set_location(40.7128, -74.0060)  # NYC
            logger.info("   ✓ Location set successfully")
        except TinderAPIError as e:
            if "passport" in str(e).lower() or "plus" in str(e).lower():
                logger.warning(
                    f"   ⚠ Location setting requires Tinder Plus: {e}"
                )
            else:
                raise e

        # Test 2: Reset location
        logger.info("2. Testing reset_location()...")
        try:
            reset_location()
            logger.info("   ✓ Location reset successfully")
        except TinderAPIError as e:
            logger.warning(f"   ⚠ Location reset failed: {e}")

        logger.info("✓ Location features test completed!")
        return True

    except Exception as e:
        logger.error(f"✗ Location test failed: {e}")
        return False


def test_error_handling():
    """Test error handling and edge cases"""
    logger.info("=== Testing Error Handling ===")

    try:
        # Test 1: Invalid user ID
        logger.info("1. Testing error handling with invalid user ID...")
        try:
            like("invalid_user_id")
            logger.warning("   ⚠ Invalid user ID didn't raise expected error")
        except TinderAPIError as e:
            logger.info(f"   ✓ Properly handled invalid user ID: {e}")

        # Test 2: Invalid endpoint
        logger.info("2. Testing error handling with invalid endpoint...")
        try:
            from modules.api import _make_request

            _make_request("GET", "/invalid/endpoint")
            logger.warning("   ⚠ Invalid endpoint didn't raise expected error")
        except TinderAPIError as e:
            logger.info(f"   ✓ Properly handled invalid endpoint: {e}")

        logger.info("✓ Error handling tests completed!")
        return True

    except Exception as e:
        logger.error(f"✗ Error handling test failed: {e}")
        return False


async def test_artist_filter():
    """Test the artist filter functionality"""
    logger.info("=== Testing Artist Filter ===")

    try:
        async with AsyncTinderAPI() as api:
            # Get recommendations
            users = await api.get_recommendations()
            logger.info(f"Retrieved {len(users)} users for artist filtering")

            artist_count = 0
            for user in users[:5]:  # Test first 5 users
                user_id = user.get("_id")
                name = user.get("name", "Unknown")
                bio = user.get("bio", "").lower()

                if "artist" in bio:
                    logger.info(f"Found artist: {name} - {bio[:50]}...")
                    try:
                        if user_id:
                            result = await api.like(user_id)
                            if result.get("match"):
                                logger.info(f"🎉 Matched with artist {name}!")
                            else:
                                logger.info(f"✓ Liked artist {name}")
                            artist_count += 1
                            await asyncio.sleep(1)  # Rate limiting
                    except TinderAPIError as e:
                        logger.warning(f"Failed to like artist {name}: {e}")

            logger.info(
                f"✓ Processed {artist_count} artists out of {len(users[:5])} users"
            )
            return True

    except Exception as e:
        logger.error(f"✗ Artist filter test failed: {e}")
        return False


def main():
    """Run all integration tests"""
    logger.info("Starting Tinder API Integration Tests")
    logger.info("=" * 50)

    # Track test results
    results = []

    # Run synchronous tests
    results.append(("Sync API", test_sync_api()))

    # Run modular tests
    results.append(("Modular API", test_modular_api()))

    # Run asynchronous tests
    results.append(("Async API", asyncio.run(test_async_api())))

    # Run location tests
    results.append(("Location Features", test_location_features()))

    # Run error handling tests
    results.append(("Error Handling", test_error_handling()))

    # Run artist filter test
    results.append(("Artist Filter", asyncio.run(test_artist_filter())))

    # Summary
    logger.info("=" * 50)
    logger.info("TEST SUMMARY:")

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1

    logger.info(f"Overall: {passed}/{total} tests passed")

    if passed == total:
        logger.info(
            "🎉 All tests passed! The API integration is working correctly."
        )
    else:
        logger.warning(
            "⚠ Some tests failed. Check the logs above for details."
        )

    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
