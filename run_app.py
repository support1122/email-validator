#!/usr/bin/env python3
"""
Simple script to run the Email Validator Web Application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def run_app():
    """Run the Flask application"""
    port = os.environ.get('PORT', '5000')
    print("Starting Email Validator Web Application...")
    print(f"🌐 The application will be available at: http://localhost:{port}")
    print("📧 You can now validate emails through the web interface!")
    print("\nPress Ctrl+C to stop the application")
    print("=" * 60)
    
    try:
        # Run the Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped. Thank you for using Email Validator!")
    except Exception as e:
        print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    print("🚀 Email Validator Web Application Launcher")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  Warning: No virtual environment detected. Consider using a virtual environment.")
    
    # Install requirements
    if install_requirements():
        # Run the application
        run_app()
    else:
        print("❌ Failed to install requirements. Please check your Python environment.")
        sys.exit(1)
