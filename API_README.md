# Tinder API Module

This module provides a clean, production-ready interface to the Tinder API, extracted from the [fbessez/Tinder](https://github.com/fbessez/Tinder) repository.

## ⚠️ Important Disclaimer

**Please use this API responsibly and in accordance with Tinder's Terms of Service.**
- This is for educational and personal use only
- Respect rate limits and don't spam the API
- Be mindful of other users' privacy
- Don't use this for commercial purposes without permission

## Features

- **Clean API**: Removed Facebook login code and simplified authentication
- **Environment-based**: Uses `.env` file for configuration
- **Production-ready**: Proper error handling, logging, and retry logic
- **Comprehensive**: Includes all major Tinder API endpoints
- **Async Support**: Both synchronous and asynchronous versions available
- **Modular Design**: Separated into focused modules for better maintainability

## Setup

1. **Install dependencies** (already in requirements.txt):
   ```bash
   pip install python-dotenv requests
   ```

2. **Create `.env` file** in your project root:
   ```env
   # Your Tinder X-Auth-Token (required)
   TINDER_AUTH_TOKEN=your_tinder_auth_token_here
   
   # Optional: Set log level (DEBUG, INFO, WARNING, ERROR)
   LOG_LEVEL=INFO
   ```

3. **Get your Tinder Auth Token**:
   - **Method 1**: Use the `phone_auth_token.py` script from the original repository
   - **Method 2**: Extract from browser network requests:
     1. Open Tinder in your browser
     2. Open Developer Tools (F12)
     3. Go to Network tab
     4. Make any action on Tinder (like, pass, etc.)
     5. Look for requests to `api.gotinder.com`
     6. Find the `X-Auth-Token` header in the request headers
   - **Method 3**: Use browser extensions that can extract auth tokens

## Usage

### Basic Example

```python
from modules.api import get_recommendations, like, dislike

# Get user recommendations
users = get_recommendations()

# Like a user
result = like(user_id)

# Dislike a user
result = dislike(user_id)
```

### Advanced Example

```python
from modules.api import (
    get_recommendations, like, get_matches, 
    send_message, set_location, TinderAPIError
)

try:
    # Get recommendations
    users = get_recommendations()
    
    # Like users with specific interests
    for user in users:
        if 'photography' in user.get('bio', '').lower():
            like(user['_id'])
    
    # Get your matches
    matches = get_matches(limit=50)
    
    # Send a message to a match
    send_message(match_id, "Hey! How's it going?")
    
    # Change location (requires Tinder Plus)
    set_location(40.7128, -74.0060)  # New York coordinates
    
except TinderAPIError as e:
    print(f"API Error: {e}")
```

### Async Example

```python
import asyncio
from modules.api_async import AsyncTinderAPI

async def main():
    async with AsyncTinderAPI() as api:
        # Get recommendations
        users = await api.get_recommendations()
        
        # Process users concurrently
        tasks = []
        for user in users[:5]:  # Limit to 5 for demo
            if 'music' in user.get('bio', '').lower():
                tasks.append(api.like(user['_id']))
        
        # Wait for all like operations
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    print(f"Error: {result}")
                elif result.get('match'):
                    print("🎉 Got a match!")

# Run the async function
asyncio.run(main())
```

### Modular API Example

```python
from modules.api_modular import (
    get_recommendations, like, set_location, TinderAPIError
)

try:
    # Use the modular API
    users = get_recommendations()
    for user in users:
        if 'travel' in user.get('bio', '').lower():
            like(user['_id'])
except TinderAPIError as e:
    print(f"Error: {e}")
```

## Available Functions

### Core Functions
- `get_recommendations()` - Get users to swipe on
- `get_recommendations_v2()` - Alternative recommendations endpoint
- `like(user_id)` - Swipe right on a user
- `dislike(user_id)` - Swipe left on a user
- `superlike(user_id)` - Super like a user

### Match Management
- `get_matches(limit=60)` - Get your matches
- `get_match_info(match_id)` - Get specific match details
- `send_message(match_id, message)` - Send a message
- `unmatch(match_id)` - Unmatch with someone

### Profile & Settings
- `get_profile()` - Get your profile data
- `update_profile(**kwargs)` - Update profile preferences
- `get_user_info(user_id)` - Get another user's info

### Location (Tinder Plus)
- `set_location(lat, lon)` - Change your location
- `reset_location()` - Reset to real location

### Other
- `get_updates(last_activity_date)` - Get activity updates
- `get_meta()` - Get account statistics
- `report_user(user_id, cause, explanation)` - Report a user

## Error Handling

The module uses a custom `TinderAPIError` exception for API-related errors:

```python
from modules.api import TinderAPIError

try:
    users = get_recommendations()
except TinderAPIError as e:
    print(f"API Error: {e}")
```

## Error Handling & Logging

The module includes comprehensive error handling and logging:

```python
import logging

# Configure logging level
logging.basicConfig(level=logging.INFO)

# The API automatically logs:
# - Request attempts and responses
# - Retry attempts with exponential backoff
# - Error details and status codes
```

### Retry Logic

The API includes automatic retry logic for:
- Network timeouts (30-second timeout)
- Server errors (5xx responses)
- Rate limiting (with exponential backoff)

## Rate Limiting

Tinder has rate limits. The module includes automatic retry logic, but you should:
- Add delays between requests (1-2 seconds)
- Handle 429 (Too Many Requests) errors gracefully
- Don't make too many requests in a short time
- Use the async version for better performance with multiple requests

## Testing

Run the integration test to validate all functionality:

```bash
python test_integration.py
```

This will test:
- Synchronous API functionality
- Asynchronous API functionality
- Modular API structure
- Error handling
- Location features
- Artist filtering

## Notes

- **Authentication**: Requires a valid Tinder X-Auth-Token
- **Tinder Plus**: Some features (location changes) require Tinder Plus
- **API Changes**: Tinder may change their API endpoints
- **Terms of Service**: Ensure your usage complies with Tinder's ToS
- **Logging**: Set `LOG_LEVEL` in your `.env` file to control verbosity 