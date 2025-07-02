#!/usr/bin/env python3
"""
Setup script for AI Voice Assistant
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
def read_requirements():
    requirements = []
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("-r"):
                requirements.append(line)
    return requirements

setup(
    name="ai-voice-assistant",
    version="1.0.0",
    author="AI Voice Assistant Team",
    author_email="",
    description="A powerful desktop application that combines voice recording, AI transcription, and intelligent chat capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/ai-voice-assistant",
    packages=find_packages(),
    py_modules=["main"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=4.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
        "build": [
            "pyinstaller>=5.0.0",
            "setuptools>=60.0.0",
            "wheel>=0.37.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-voice-assistant=main:main",
        ],
        "gui_scripts": [
            "ai-voice-assistant-gui=main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/username/ai-voice-assistant/issues",
        "Source": "https://github.com/username/ai-voice-assistant",
        "Documentation": "https://github.com/username/ai-voice-assistant#readme",
        "Changelog": "https://github.com/username/ai-voice-assistant/blob/main/CHANGELOG.md",
    },
    keywords=[
        "voice",
        "assistant",
        "ai",
        "transcription",
        "whisper",
        "speech-to-text",
        "chat",
        "lm-studio",
        "desktop",
        "gui",
    ],
    include_package_data=True,
    zip_safe=False,
)
