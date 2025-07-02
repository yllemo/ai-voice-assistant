#!/usr/bin/env python3
"""
Development setup script for AI Voice Assistant
Sets up development environment and tools
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description or cmd}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def check_python_version():
    """Check Python version compatibility"""
    print("Checking Python version...")
    
    version = sys.version_info
    if version.major != 3 or version.minor < 8:
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")
    return True

def setup_virtual_environment():
    """Set up virtual environment"""
    print("Setting up virtual environment...")
    
    if os.path.exists("venv"):
        print("Virtual environment already exists")
        return True
    
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    print("✅ Virtual environment created")
    print("To activate:")
    
    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    
    return True

def install_dependencies():
    """Install development dependencies"""
    print("Installing dependencies...")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        print("⚠️  Warning: Not in virtual environment")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return False
    
    commands = [
        "pip install --upgrade pip",
        "pip install -r requirements.txt",
        "pip install -r requirements-dev.txt"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            return False
    
    return True

def install_system_dependencies():
    """Install system-level dependencies"""
    print("Checking system dependencies...")
    
    system = platform.system().lower()
    
    if system == "linux":
        print("For Ubuntu/Debian systems, you may need:")
        print("  sudo apt-get update")
        print("  sudo apt-get install -y portaudio19-dev python3-pyaudio")
        
    elif system == "darwin":  # macOS
        print("For macOS with Homebrew:")
        print("  brew install portaudio")
        
    elif system == "windows":
        print("For Windows:")
        print("  If PyAudio fails to install, try:")
        print("  pip install pipwin")
        print("  pipwin install pyaudio")
    
    return True

def setup_git_hooks():
    """Set up Git pre-commit hooks"""
    print("Setting up Git hooks...")
    
    if not os.path.exists(".git"):
        print("Not a Git repository, skipping hooks setup")
        return True
    
    commands = [
        "pip install pre-commit",
        "pre-commit install"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print("Failed to set up Git hooks, continuing...")
            break
    else:
        print("✅ Git hooks configured")
    
    return True

def run_initial_tests():
    """Run initial tests to verify setup"""
    print("Running initial tests...")
    
    # Test basic imports
    test_imports = [
        "import tkinter",
        "import threading", 
        "import wave",
        "import tempfile",
        "import os",
        "import requests",
    ]
    
    for test in test_imports:
        try:
            exec(test)
            print(f"✅ {test}")
        except ImportError as e:
            print(f"❌ {test} - {e}")
            return False
    
    # Try to import PyAudio and Whisper (might fail on some systems)
    optional_imports = [
        ("import pyaudio", "PyAudio - needed for audio recording"),
        ("import whisper", "Whisper - needed for transcription"),
    ]
    
    for test, description in optional_imports:
        try:
            exec(test)
            print(f"✅ {test}")
        except ImportError as e:
            print(f"⚠️  {test} - {description} - {e}")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("Creating project directories...")
    
    dirs = ["temp", "logs", "recordings"]
    
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory}/")
        else:
            print(f"📁 {directory}/ already exists")
    
    return True

def main():
    """Main setup process"""
    print("AI Voice Assistant - Development Setup")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    
    # Setup steps
    steps = [
        ("Check Python version", check_python_version),
        ("Create directories", create_directories),
        ("Set up virtual environment", setup_virtual_environment),
        ("Install dependencies", install_dependencies),
        ("Check system dependencies", install_system_dependencies),
        ("Set up Git hooks", setup_git_hooks),
        ("Run initial tests", run_initial_tests),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"❌ {step_name} failed!")
            failed_steps.append(step_name)
        else:
            print(f"✅ {step_name} completed!")
    
    print("\n" + "="*60)
    
    if failed_steps:
        print("⚠️  Setup completed with issues:")
        for step in failed_steps:
            print(f"  - {step}")
        print("\nPlease review the errors above and fix them manually.")
    else:
        print("🎉 Development setup completed successfully!")
    
    print("\nNext steps:")
    print("1. Activate virtual environment (if not already active)")
    print("2. Run: python main.py")
    print("3. Test the application")
    print("4. Start developing!")
    
    print("\nUseful commands:")
    print("  python main.py          - Run the application")
    print("  python -m pytest        - Run tests")
    print("  black main.py           - Format code")
    print("  flake8 main.py          - Check code style")
    print("  python scripts/build.py - Build executable")

if __name__ == "__main__":
    main()
