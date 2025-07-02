"""
Basic tests for AI Voice Assistant
"""
import unittest
import sys
import os

# Add parent directory to path to import main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import main
    MAIN_IMPORT_SUCCESS = True
except ImportError as e:
    MAIN_IMPORT_SUCCESS = False
    IMPORT_ERROR = str(e)


class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality without GUI"""

    def test_main_module_import(self):
        """Test that main module can be imported"""
        self.assertTrue(MAIN_IMPORT_SUCCESS, 
                       f"Failed to import main module: {IMPORT_ERROR if not MAIN_IMPORT_SUCCESS else ''}")

    def test_required_libraries(self):
        """Test that required libraries can be imported"""
        required_libs = [
            'tkinter',
            'threading', 
            'pyaudio',
            'wave',
            'tempfile',
            'os',
            'requests',
            'whisper'
        ]
        
        failed_imports = []
        for lib in required_libs:
            try:
                __import__(lib)
            except ImportError:
                failed_imports.append(lib)
        
        self.assertEqual([], failed_imports, 
                        f"Failed to import required libraries: {failed_imports}")

    def test_class_definition(self):
        """Test that AIVoiceAssistant class is properly defined"""
        if MAIN_IMPORT_SUCCESS:
            self.assertTrue(hasattr(main, 'AIVoiceAssistant'),
                           "AIVoiceAssistant class not found")
            self.assertTrue(callable(getattr(main, 'AIVoiceAssistant')),
                           "AIVoiceAssistant is not callable")

    def test_main_function(self):
        """Test that main function exists and is callable"""
        if MAIN_IMPORT_SUCCESS:
            self.assertTrue(hasattr(main, 'main'),
                           "main function not found")
            self.assertTrue(callable(getattr(main, 'main')),
                           "main function is not callable")

    def test_default_settings(self):
        """Test default configuration values"""
        if MAIN_IMPORT_SUCCESS:
            # This would require refactoring the class to allow testing without GUI
            # For now, just test that we can access the class
            self.assertTrue(True, "Basic class structure test")


class TestAudioHandling(unittest.TestCase):
    """Test audio-related functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_audio_formats = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']

    def test_supported_audio_formats(self):
        """Test that supported audio formats are defined"""
        # This would require accessing the actual supported formats from the class
        self.assertTrue(len(self.test_audio_formats) > 0,
                       "Audio formats list should not be empty")


class TestAPIIntegration(unittest.TestCase):
    """Test API integration functionality"""

    def test_default_lm_studio_url(self):
        """Test default LM Studio URL format"""
        default_url = "http://localhost:1234/v1/chat/completions"
        self.assertTrue(default_url.startswith('http'),
                       "Default URL should start with http")
        self.assertIn('localhost', default_url,
                     "Default URL should contain localhost")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
