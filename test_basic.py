#!/usr/bin/env python3
"""
Basic Tinder API Test Script
Tests imports and structure without requiring a real Tinder token.
"""

import os
import sys
from unittest.mock import MagicMock, patch


def test_imports():
    """Test that all modules can be imported correctly"""
    print("Testing imports...")
    
    try:
        # Test main API
        from modules.api import (TinderAPIError, dislike, get_matches,
                                 get_recommendations, like, reset_location,
                                 set_location)
        print("✓ Main API imports successful")
        
        # Test modular API
        from modules.api_modular import \
            get_recommendations as modular_get_recommendations
        from modules.api_modular import like as modular_like
        from modules.api_modular import set_location as modular_set_location
        print("✓ Modular API imports successful")
        
        # Test async API
        from modules.api_async import AsyncTinderAPI
        print("✓ Async API imports successful")
        
        # Test individual modules
        from modules.auth import TinderAPIError as AuthError
        from modules.location import set_location as loc_set_location
        from modules.recs import get_recommendations as recs_get_recs
        from modules.swipe import like as swipe_like
        print("✓ Individual module imports successful")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_error_handling():
    """Test error handling without making real API calls"""
    print("\nTesting error handling...")
    
    try:
        from modules.api import TinderAPIError

        # Test that TinderAPIError is properly defined
        assert issubclass(TinderAPIError, Exception)
        print("✓ TinderAPIError class properly defined")
        
        # Test error instantiation
        error = TinderAPIError("Test error")
        assert str(error) == "Test error"
        print("✓ Error instantiation works")
        
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False


def test_mock_api_calls():
    """Test API structure with mocked responses"""
    print("\nTesting API structure with mocks...")
    
    try:
        from modules.api import get_recommendations, like

        # Mock the _make_request function
        with patch('modules.api._make_request') as mock_request:
            # Mock successful response
            mock_request.return_value = {
                'results': [
                    {
                        '_id': 'test_user_1',
                        'name': 'Test User',
                        'bio': 'Test bio'
                    }
                ]
            }
            
            # Test get_recommendations structure
            result = get_recommendations()
            assert 'results' in result
            assert len(result['results']) > 0
            assert '_id' in result['results'][0]
            print("✓ get_recommendations structure correct")
            
            # Mock like response
            mock_request.return_value = {'match': False}
            like_result = like('test_user_1')
            assert 'match' in like_result
            print("✓ like function structure correct")
        
        return True
        
    except Exception as e:
        print(f"✗ Mock API test failed: {e}")
        return False


def test_async_structure():
    """Test async API structure"""
    print("\nTesting async API structure...")
    
    try:
        from modules.api_async import AsyncTinderAPI

        # Test class instantiation (without real client)
        with patch('modules.api_async.httpx.AsyncClient'):
            api = AsyncTinderAPI()
            assert hasattr(api, 'get_recommendations')
            assert hasattr(api, 'like')
            assert hasattr(api, 'dislike')
            assert hasattr(api, 'set_location')
            print("✓ AsyncTinderAPI has required methods")
        
        return True
        
    except Exception as e:
        print(f"✗ Async structure test failed: {e}")
        return False


def test_environment_handling():
    """Test environment variable handling"""
    print("\nTesting environment handling...")
    
    try:
        from modules.auth import get_auth_token

        # Test missing token
        with patch.dict(os.environ, {}, clear=True):
            try:
                get_auth_token()
                print("✗ Should have raised error for missing token")
                return False
            except Exception as e:
                if "TINDER_AUTH_TOKEN" in str(e):
                    print("✓ Properly handles missing auth token")
                else:
                    print(f"✗ Unexpected error: {e}")
                    return False
        
        # Test with token
        with patch.dict(os.environ, {'TINDER_AUTH_TOKEN': 'test_token'}):
            token = get_auth_token()
            assert token == 'test_token'
            print("✓ Properly reads auth token from environment")
        
        return True
        
    except Exception as e:
        print(f"✗ Environment handling test failed: {e}")
        return False


def main():
    """Run all basic tests"""
    print("Tinder API Basic Tests")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Error Handling", test_error_handling),
        ("Mock API Calls", test_mock_api_calls),
        ("Async Structure", test_async_structure),
        ("Environment Handling", test_environment_handling),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print("\n" + "=" * 40)
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed! The API structure is correct.")
        print("\nNext steps:")
        print("1. Set up your .env file with TINDER_AUTH_TOKEN")
        print("2. Run: python test_integration.py")
        print("3. Or run: python main.py")
    else:
        print("⚠ Some tests failed. Check the output above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 