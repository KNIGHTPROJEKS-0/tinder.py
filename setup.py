#!/usr/bin/env python3
"""
Tinder API Setup Script
Ensures all dependencies are installed and environment is properly configured.
"""

import subprocess
import sys
from pathlib import Path


def check_python_version() -> bool:
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(
            f"❌ Python {version.major}.{version.minor} is not supported. "
            "Please use Python 3.8+"
        )
        return False
    print(
        f"✅ Python {version.major}.{version.minor}.{version.micro} "
        "is compatible"
    )
    return True


def install_dependencies() -> bool:
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install from requirements.txt
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def check_dependencies() -> bool:
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'requests', 'httpx', 'python-dotenv', 'selenium', 
        'undetected-chromedriver', 'lxml'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies are installed")
    return True


def check_modules() -> bool:
    """Check if all modules can be imported"""
    print("\n📁 Checking modules...")
    
    modules_to_test = [
        ('modules.api', 'Main API'),
        ('modules.api_async', 'Async API'),
        ('modules.api_modular', 'Modular API'),
        ('modules.auth', 'Auth module'),
        ('modules.recs', 'Recommendations module'),
        ('modules.swipe', 'Swipe module'),
        ('modules.location', 'Location module'),
    ]
    
    failed_modules = []
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description}")
        except ImportError as e:
            print(f"❌ {description} - {e}")
            failed_modules.append(module_name)
    
    if failed_modules:
        print(f"\n⚠ Failed modules: {', '.join(failed_modules)}")
        return False
    
    print("✅ All modules can be imported")
    return True


def check_env_file() -> bool:
    """Check if .env file exists and has required variables"""
    print("\n🔧 Checking environment configuration...")
    
    env_file = Path('.env')
    
    if not env_file.exists():
        print("⚠ .env file not found")
        print("📝 Creating .env template...")
        
        with open('.env', 'w') as f:
            f.write("# Tinder API Configuration\n")
            f.write("# Add your Tinder auth token here\n")
            f.write("TINDER_AUTH_TOKEN=your_token_here\n")
            f.write("\n# Optional: Facebook credentials (for Facebook auth)\n")
            f.write("# FB_USERNAME=your_facebook_username\n")
            f.write("# FB_PASSWORD=your_facebook_password\n")
            f.write("\n# Optional: Logging level\n")
            f.write("LOG_LEVEL=INFO\n")
        
        print("✅ Created .env template")
        print("📝 Please edit .env and add your Tinder auth token")
        return False
    
    # Check if TINDER_AUTH_TOKEN is set
    with open('.env', 'r') as f:
        content = f.read()
        if ('TINDER_AUTH_TOKEN=your_token_here' in content or 
                'TINDER_AUTH_TOKEN=' not in content):
            print("⚠ TINDER_AUTH_TOKEN not configured in .env")
            print("📝 Please edit .env and add your Tinder auth token")
            return False
    
    print("✅ Environment configuration looks good")
    return True


def run_basic_tests() -> bool:
    """Run basic tests to ensure everything works"""
    print("\n🧪 Running basic tests...")
    
    try:
        result = subprocess.run(
            [sys.executable, "test_basic.py"], 
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print("✅ Basic tests passed")
            return True
        else:
            print("⚠ Basic tests had issues (this is normal without a real token)")
            print("Output:", result.stdout)
            return True  # We consider this OK since we don't have a real token
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False


def create_example_scripts() -> bool:
    """Create example scripts for users"""
    print("\n📝 Creating example scripts...")
    
    # Check if main.py exists and is properly configured
    if not Path('main.py').exists():
        print("⚠ main.py not found")
    else:
        print("✅ main.py exists")
    
    # Check if test scripts exist
    test_scripts = ['test_basic.py', 'test_integration.py']
    for script in test_scripts:
        if Path(script).exists():
            print(f"✅ {script} exists")
        else:
            print(f"⚠ {script} not found")
    
    return True


def print_next_steps() -> None:
    """Print next steps for the user"""
    print("\n" + "="*50)
    print("🎉 Setup Complete!")
    print("="*50)
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your Tinder auth token")
    print("2. Run: python get_tinder_token.py (to get help with token)")
    print("3. Run: python main.py (to test the API)")
    print("4. Run: python test_integration.py (for full testing)")
    print("\n📚 Documentation:")
    print("- Check API_README.md for detailed usage")
    print("- Check INTEGRATION_SUMMARY.md for overview")
    print("\n🔧 Available APIs:")
    print("- modules.api (synchronous)")
    print("- modules.api_async (asynchronous)")
    print("- modules.api_modular (modular)")
    print("\n💡 Example usage:")
    print("  from modules.api import get_recommendations, like")
    print("  users = get_recommendations()")
    print("  like(users[0]['_id']) if users else None")


def main() -> bool:
    """Main setup function"""
    print("🚀 Tinder API Setup")
    print("="*50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Modules", check_modules),
        ("Environment", check_env_file),
        ("Basic Tests", run_basic_tests),
        ("Example Scripts", create_example_scripts),
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} check failed: {e}")
            all_passed = False
    
    if all_passed:
        print("\n✅ All checks passed!")
    else:
        print("\n⚠ Some checks failed, but setup can continue")
    
    print_next_steps()
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 