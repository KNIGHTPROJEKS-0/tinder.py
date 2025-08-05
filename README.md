# 🎯 Tinder API Integration

A comprehensive, production-ready Python library for interacting with the Tinder API. This project provides clean, modular, and well-documented APIs for Tinder automation.

## ✨ Features

- **Multiple API Interfaces**: Synchronous, asynchronous, and modular APIs
- **Production Ready**: Comprehensive error handling, logging, and retry logic
- **Type Safety**: Full type hints throughout the codebase
- **Environment Management**: Secure token handling via environment variables
- **Comprehensive Testing**: Built-in test suites for validation
- **Documentation**: Complete setup and usage guides

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd tinder.py

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup

```bash
# Create .env file with your Tinder auth token
echo "TINDER_AUTH_TOKEN=your_token_here" > .env

# Or use the helper script
python get_tinder_token.py
```

### 3. Basic Usage

```python
from modules.api import get_recommendations, like

# Get user recommendations
users = get_recommendations()

# Like users with specific interests
for user in users:
    if 'music' in user.get('bio', '').lower():
        like(user['_id'])
```

## 📚 API Interfaces

### 1. Synchronous API (`modules.api`)

```python
from modules.api import get_recommendations, like, dislike, get_matches

# Get recommendations
users = get_recommendations()

# Like a user
result = like(user_id)

# Get matches
matches = get_matches(limit=50)
```

### 2. Asynchronous API (`modules.api_async`)

```python
from modules.api_async import AsyncTinderAPI

async with AsyncTinderAPI() as api:
    users = await api.get_recommendations()
    result = await api.like(user_id)
```

### 3. Modular API (`modules.api_modular`)

```python
from modules.api_modular import get_recommendations, like

users = get_recommendations()
like(user_id)
```

## 🔧 Available Functions

### Core Functions
- `get_recommendations()` - Get user recommendations
- `like(user_id)` - Like a user (swipe right)
- `dislike(user_id)` - Dislike a user (swipe left)
- `superlike(user_id)` - Super like a user
- `get_matches(limit)` - Get user matches

### Profile Management
- `get_profile()` - Get user's own profile
- `update_profile(**kwargs)` - Update profile settings
- `get_user_info(user_id)` - Get specific user info

### Messaging
- `send_message(match_id, message)` - Send message to match
- `unmatch(match_id)` - Unmatch with user

### Location Features (Tinder Plus)
- `set_location(lat, lon)` - Set location
- `reset_location()` - Reset to real location

### Advanced Features
- `get_updates(last_activity_date)` - Get updates
- `get_meta()` - Get meta data
- `report_user(user_id, cause, explanation)` - Report user

## 🧪 Testing

```bash
# Run basic tests (no token required)
python test_basic.py

# Run full integration tests (requires token)
python test_integration.py

# Run setup validation
python setup.py
```

## 📁 Project Structure

```
tinder.py/
├── modules/
│   ├── __init__.py              # Package exports
│   ├── api.py                   # Main API (sync)
│   ├── api_async.py             # Async API
│   ├── api_modular.py           # Modular interface
│   ├── auth.py                  # Authentication
│   ├── recs.py                  # Recommendations
│   ├── swipe.py                 # Swipe actions
│   └── location.py              # Location features
├── Tinder/                      # Original repository
├── main.py                      # Music example
├── example_modular.py           # Comprehensive examples
├── test_basic.py                # Basic validation
├── test_integration.py          # Full integration tests
├── setup.py                     # Environment setup
├── get_tinder_token.py          # Token helper
├── API_README.md                # Detailed documentation
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🔐 Authentication

### Getting Your Tinder Auth Token

1. **Browser Method**:
   - Open Tinder in your browser
   - Open Developer Tools (F12)
   - Go to Network tab
   - Make any action on Tinder
   - Look for requests to 'api.gotinder.com'
   - Find the 'X-Auth-Token' header

2. **Helper Script**:
   ```bash
   python get_tinder_token.py
   ```

### Environment Setup

Create a `.env` file in the project root:

```env
TINDER_AUTH_TOKEN=your_tinder_auth_token_here
LOG_LEVEL=INFO
```

## ⚠️ Important Notes

- **Rate Limiting**: The API includes built-in rate limiting and retry logic
- **Tinder Plus Features**: Location features require Tinder Plus subscription
- **Responsible Use**: Please use this API responsibly and in accordance with Tinder's terms of service
- **Token Security**: Never commit your auth token to version control

## 🛠️ Development

### Adding New Features

1. Add functions to the appropriate module (`modules/api.py`, `modules/api_async.py`)
2. Update the modular interface (`modules/api_modular.py`)
3. Add tests to `test_integration.py`
4. Update documentation

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add comprehensive docstrings
- Include error handling

## 📄 License

This project is for educational purposes. Please use responsibly and in accordance with Tinder's terms of service.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the documentation in `API_README.md`
- Review the test files for usage examples
- Open an issue on GitHub

---

**Disclaimer**: This project is for educational purposes. Use responsibly and in accordance with Tinder's terms of service.
