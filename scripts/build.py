#!/usr/bin/env python3
"""
Build script for AI Voice Assistant
Creates executable files for different platforms
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description or cmd}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def clean_build():
    """Clean previous build artifacts"""
    print("Cleaning build artifacts...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__', '*.egg-info']
    for dir_pattern in dirs_to_clean:
        for path in Path('.').glob(dir_pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
            elif path.is_file():
                path.unlink()
                print(f"Removed file: {path}")

def install_dependencies():
    """Install build dependencies"""
    print("Installing build dependencies...")
    
    commands = [
        "pip install --upgrade pip",
        "pip install -r requirements.txt", 
        "pip install pyinstaller",
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Installing dependencies: {cmd}"):
            return False
    return True

def build_executable():
    """Build executable using PyInstaller"""
    print("Building executable...")
    
    # Determine platform-specific options
    system = platform.system().lower()
    
    base_cmd = [
        "pyinstaller",
        "--onefile",
        "--name=ai-voice-assistant",
        "--add-data=README.md;.",
        "--hidden-import=tkinter",
        "--hidden-import=pyaudio", 
        "--hidden-import=whisper",
        "--hidden-import=requests",
    ]
    
    if system == "windows":
        base_cmd.extend([
            "--windowed",  # Hide console on Windows
            "--icon=icon.ico"  # Add icon if available
        ])
    elif system == "darwin":  # macOS
        base_cmd.extend([
            "--windowed",
            "--icon=icon.icns"  # Add icon if available
        ])
    
    # Add the main script
    base_cmd.append("main.py")
    
    cmd = " ".join(base_cmd)
    return run_command(cmd, "Building executable with PyInstaller")

def create_archive():
    """Create distribution archive"""
    print("Creating distribution archive...")
    
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    # Create archive name
    archive_name = f"ai-voice-assistant-{system}-{arch}"
    
    if system == "windows":
        # Create ZIP for Windows
        cmd = f"powershell Compress-Archive -Path dist/* -DestinationPath {archive_name}.zip"
    else:
        # Create tar.gz for Unix-like systems
        cmd = f"tar -czf {archive_name}.tar.gz -C dist ."
    
    return run_command(cmd, f"Creating {archive_name} archive")

def run_tests():
    """Run tests before building"""
    print("Running tests...")
    
    if not run_command("python -m pytest tests/ -v", "Running unit tests"):
        print("Tests failed. Aborting build.")
        return False
    
    return True

def main():
    """Main build process"""
    print("AI Voice Assistant - Build Script")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("Error: main.py not found. Run this script from the project root.")
        sys.exit(1)
    
    # Build steps
    steps = [
        ("Clean build artifacts", clean_build),
        ("Install dependencies", install_dependencies),
        ("Run tests", run_tests),
        ("Build executable", build_executable),
        ("Create archive", create_archive),
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if callable(step_func):
            if not step_func():
                print(f"❌ {step_name} failed!")
                sys.exit(1)
        else:
            step_func()
        print(f"✅ {step_name} completed!")
    
    print("\n🎉 Build completed successfully!")
    print("\nBuild artifacts:")
    
    # List build outputs
    if os.path.exists("dist"):
        for item in os.listdir("dist"):
            print(f"  - dist/{item}")
    
    # List archives
    for ext in [".zip", ".tar.gz"]:
        for archive in Path(".").glob(f"*{ext}"):
            print(f"  - {archive}")

if __name__ == "__main__":
    main()
