# Contributing to AI Voice Assistant

Thank you for your interest in contributing to the AI Voice Assistant! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** to avoid duplicates
2. **Use the issue templates** when available
3. **Provide detailed information**:
   - Operating system and version
   - Python version
   - Error messages and stack traces
   - Steps to reproduce the issue

### Suggesting Features

1. **Check existing feature requests** first
2. **Describe the use case** clearly
3. **Explain the expected behavior**
4. **Consider implementation complexity**

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Write clean, documented code**
4. **Test your changes thoroughly**
5. **Commit with clear messages** (`git commit -m 'Add amazing feature'`)
6. **Push to your branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Local Development

```bash
# Clone your fork
git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Testing

```bash
# Run basic functionality tests
python -c "import main; print('Import successful')"

# Test audio recording (requires microphone)
# Test LM Studio connection (requires running LM Studio)
# Test transcription (requires Whisper model)
```

## 📝 Code Style

### Python Guidelines

- Follow **PEP 8** style guide
- Use **meaningful variable names**
- Add **docstrings** for functions and classes
- Keep **functions focused** and small
- Use **type hints** where appropriate

### Code Example

```python
def transcribe_audio(self, audio_file_path: str) -> str:
    """
    Transcribe audio file using Whisper model.
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
        
    Raises:
        Exception: If transcription fails
    """
    try:
        result = self.whisper_model.transcribe(audio_file_path)
        return result["text"].strip()
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")
```

### UI Guidelines

- Maintain **consistent styling** with existing dark theme
- Use **descriptive widget names**
- Keep **responsive layout** in mind
- Add **proper error handling** for UI operations

## 🎯 Priority Areas

### High Priority
- **Bug fixes** and stability improvements
- **Performance optimizations**
- **Cross-platform compatibility**
- **Security enhancements**

### Medium Priority
- **New AI provider integrations**
- **Audio quality improvements**
- **User experience enhancements**
- **Documentation updates**

### Low Priority
- **Advanced features** from IMPROVEMENTS.md
- **UI theme variations**
- **Additional file format support**

## 🧪 Testing Guidelines

### Manual Testing Checklist

- [ ] Audio recording starts/stops correctly
- [ ] File loading works with various formats
- [ ] Transcription produces reasonable results
- [ ] LM Studio connection is stable
- [ ] Chat functionality works as expected
- [ ] UI remains responsive during operations
- [ ] Error messages are helpful

### Test Cases to Consider

1. **Audio Recording**
   - Various microphone qualities
   - Different recording durations
   - Background noise scenarios

2. **File Loading**
   - Different audio formats (WAV, MP3, etc.)
   - Large files (>10MB)
   - Corrupted files

3. **AI Integration**
   - LM Studio connection failures
   - Model loading issues
   - Network timeouts

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Functionality has been tested
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear
- [ ] No sensitive information is included

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Manual testing performed
- [ ] Edge cases considered

## Additional Notes
Any additional information or context
```

## 🐛 Issue Templates

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g. Windows 10]
- Python Version: [e.g. 3.9.1]
- App Version: [e.g. v1.0.0]

**Additional context**
Add any other context about the problem.
```

### Feature Request Template

```markdown
**Feature Description**
A clear description of what you want to happen.

**Use Case**
Explain the problem this feature would solve.

**Proposed Solution**
Describe how you envision this working.

**Alternatives Considered**
Any alternative solutions you've thought about.

**Additional Context**
Any other context or screenshots.
```

## 🎉 Recognition

Contributors will be recognized in the following ways:

- **README acknowledgments** for significant contributions
- **Release notes mentions** for bug fixes and features
- **Contributor list** maintenance in the repository

## 📞 Getting Help

If you need help contributing:

1. **Check existing documentation** first
2. **Search closed issues** for similar questions
3. **Open a discussion** for general questions
4. **Join our community** (if applicable)

Thank you for helping make AI Voice Assistant better! 🚀
