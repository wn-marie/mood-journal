#!/usr/bin/env python3
"""
Mood Journal - Quick Start Script
This script helps you get the Mood Journal running quickly.
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("\n🔧 Creating .env file...")
        with open('.env', 'w') as f:
            f.write("# Mood Journal Environment Configuration\n")
            f.write("HUGGINGFACE_API_KEY=your_api_key_here\n")
            f.write("INTASEND_API_KEY=your_intasend_api_key_here\n")
            f.write("INTASEND_PUBLISHABLE_KEY=your_intasend_publishable_key_here\n")
            f.write("FLASK_ENV=development\n")
            f.write("FLASK_DEBUG=True\n")
            f.write("SECRET_KEY=your-secret-key-here\n")
        print("✅ .env file created!")
        print("💡 You can add your API keys to the .env file for better performance")
        print("   - Hugging Face API key for sentiment analysis")
        print("   - IntaSend API keys for payment processing")
    else:
        print("✅ .env file already exists")

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting Mood Journal...")
    print("=" * 50)
    print("🌐 Application will be available at: http://localhost:5000")
    print("📱 Open this URL in your browser to use the app")
    print("💳 Navigate to 'Monetization' to see IntaSend integration")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for using Mood Journal!")

def main():
    """Main function to set up and run the application"""
    print("🌟 Welcome to Mood Journal - AI-Powered Emotion Tracker")
    print("🎯 SDG 3: Good Health and Well-being")
    print("💳 Integrated with IntaSend for Monetization")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create environment file
    create_env_file()
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()

import os
print(os.listdir(r'c:\Users\Admin\Desktop\SDG3 mood-journal'))

import os
print(os.listdir(r'c:\Users\Admin\Desktop\SDG3 mood-journal'))
