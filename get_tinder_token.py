#!/usr/bin/env python3
"""
Tinder Auth Token Helper
This script helps you get your Tinder auth token using phone authentication.
Based on the original repository's phone_auth_token.py
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_token_from_env():
    """Get token from environment variable"""
    token = os.getenv('TINDER_AUTH_TOKEN')
    if token:
        print(f"✅ Found Tinder token in environment: {token[:10]}...")
        return token
    return None

def get_token_from_input():
    """Get token from user input"""
    print("\n📱 Tinder Auth Token Setup")
    print("=" * 40)
    print("To get your Tinder auth token:")
    print("1. Open Tinder in your browser")
    print("2. Open Developer Tools (F12)")
    print("3. Go to Network tab")
    print("4. Make any action on Tinder (like, pass, etc.)")
    print("5. Look for requests to 'api.gotinder.com'")
    print("6. Find the 'X-Auth-Token' header in the request headers")
    print("\nAlternative method:")
    print("1. Use the phone_auth_token.py script from the Tinder/ directory")
    print("2. Follow the SMS verification process")
    
    token = input("\n🔑 Enter your Tinder auth token: ").strip()
    
    if not token:
        print("❌ No token provided")
        return None
    
    return token

def save_token_to_env(token):
    """Save token to .env file"""
    env_file = '.env'
    
    # Read existing .env file
    env_content = {}
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key] = value
    
    # Update or add TINDER_AUTH_TOKEN
    env_content['TINDER_AUTH_TOKEN'] = token
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        for key, value in env_content.items():
            f.write(f"{key}={value}\n")
    
    print(f"✅ Token saved to {env_file}")

def test_token(token):
    """Test if the token works"""
    try:
        from modules.api import get_profile

        # Temporarily set the environment variable
        os.environ['TINDER_AUTH_TOKEN'] = token
        
        # Try to get profile
        profile = get_profile()
        if profile and 'name' in profile:
            print(f"✅ Token is valid! Connected as: {profile['name']}")
            return True
        else:
            print("❌ Token appears to be invalid")
            return False
            
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False

def main():
    """Main function"""
    print("🎯 Tinder Auth Token Helper")
    print("=" * 40)
    
    # Check if token already exists
    existing_token = get_token_from_env()
    if existing_token:
        print("Found existing token. Testing...")
        if test_token(existing_token):
            print("✅ Existing token is working!")
            return
        else:
            print("❌ Existing token is invalid. Please provide a new one.")
    
    # Get new token
    token = get_token_from_input()
    if not token:
        print("❌ No token provided. Exiting.")
        return
    
    # Test the token
    print("\n🧪 Testing token...")
    if test_token(token):
        # Save to .env file
        save_token_to_env(token)
        print("\n🎉 Setup complete! You can now use the Tinder API.")
        print("Run: python main.py")
    else:
        print("\n❌ Token validation failed. Please check your token and try again.")

if __name__ == "__main__":
    main() 