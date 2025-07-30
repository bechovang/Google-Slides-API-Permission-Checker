# Maintenance Guide - Google Slides API Permission Checker

## 🔧 Development Setup

### Environment Setup

1. **Python Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Google Cloud Setup**
   - Create a Google Cloud Project
   - Enable Google Slides API
   - Create OAuth 2.0 credentials
   - Download credentials as `credentials.json`

### Code Structure

```
Google-Slides-API-Permission-Checker/
├── main.py              # Main application file
├── credentials.json     # Google OAuth credentials (user-provided)
├── token.json          # Generated OAuth tokens
├── requirements.txt     # Python dependencies
├── README.md           # User documentation
├── MAINTAIN.md         # This maintenance guide
└── slides_content_*.json # Generated content files
```

## 🧪 Testing

### Unit Testing

Create test files for each component:

```python
# test_google_slides_checker.py
import unittest
from main import GoogleSlidesChecker

class TestGoogleSlidesChecker(unittest.TestCase):
    def setUp(self):
        self.checker = GoogleSlidesChecker()
    
    def test_extract_presentation_id(self):
        # Test URL extraction
        url = "https://docs.google.com/presentation/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"
        result = self.checker.extract_presentation_id(url)
        self.assertEqual(result, "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")
    
    def test_extract_presentation_id_direct(self):
        # Test direct ID
        result = self.checker.extract_presentation_id("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")
        self.assertEqual(result, "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

Test the full workflow:

```python
# test_integration.py
import unittest
from unittest.mock import patch, MagicMock
from main import GoogleSlidesChecker

class TestIntegration(unittest.TestCase):
    @patch('main.build')
    def test_full_workflow(self, mock_build):
        # Mock the Google API service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Mock presentation response
        mock_presentation = {
            'title': 'Test Presentation',
            'slides': [
                {
                    'objectId': 'slide_1',
                    'pageElements': [
                        {
                            'objectId': 'text_1',
                            'shape': {
                                'text': {
                                    'textElements': [
                                        {'textRun': {'content': 'Test text'}}
                                    ]
                                }
                            }
                        }
                    ]
                }
            ]
        }
        
        mock_service.presentations().get().execute.return_value = mock_presentation
        
        # Test the workflow
        checker = GoogleSlidesChecker()
        # ... test implementation
```

## 🔄 Version Management

### Versioning Strategy

Use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes in API or major feature additions
- **MINOR**: New features or improvements
- **PATCH**: Bug fixes and minor improvements

### Release Process

1. **Update version in code**
   ```python
   # Add to main.py
   __version__ = "1.0.0"
   ```

2. **Create release notes**
   ```markdown
   # Release Notes v1.0.0
   
   ## New Features
   - Initial release
   - OAuth authentication
   - Presentation access testing
   - Content extraction
   
   ## Bug Fixes
   - None
   
   ## Breaking Changes
   - None
   ```

3. **Tag the release**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

## 🐛 Bug Fixes

### Common Issues and Solutions

1. **OAuth Token Expiration**
   ```python
   # In setup_credentials method
   if self.creds and self.creds.expired and self.creds.refresh_token:
       try:
           self.creds.refresh(Request())
       except Exception as e:
           print(f"Token refresh failed: {e}")
           # Remove invalid token file
           if os.path.exists(self.token_file):
               os.remove(self.token_file)
   ```

2. **API Rate Limiting**
   ```python
   import time
   
   def test_presentation_access(self, presentation_id):
       max_retries = 3
       for attempt in range(max_retries):
           try:
               # API call
               return True, presentation
           except HttpError as e:
               if e.resp.status == 429:  # Rate limit
                   if attempt < max_retries - 1:
                       time.sleep(2 ** attempt)  # Exponential backoff
                       continue
               raise
   ```

3. **Invalid Presentation ID**
   ```python
   def extract_presentation_id(self, url):
       # Add validation
       presentation_id = super().extract_presentation_id(url)
       if presentation_id and len(presentation_id) < 10:
           return None  # Too short to be valid
       return presentation_id
   ```

## 🔒 Security Updates

### OAuth Security

1. **Token Security**
   ```python
   import os
   from pathlib import Path
   
   def secure_token_storage(self):
       # Set restrictive permissions on token file
       token_path = Path(self.token_file)
       token_path.chmod(0o600)  # Owner read/write only
   ```

2. **Credential Validation**
   ```python
   def validate_credentials(self):
       if not os.path.exists(self.credentials_file):
           return False
       
       try:
           with open(self.credentials_file, 'r') as f:
               creds_data = json.load(f)
           
           required_fields = ['installed', 'client_id', 'client_secret']
           return all(field in creds_data for field in required_fields)
       except (json.JSONDecodeError, KeyError):
           return False
   ```

## 📊 Monitoring and Logging

### Add Logging

```python
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('slides_checker.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class GoogleSlidesChecker:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # ... rest of init
    
    def test_presentation_access(self, presentation_id):
        self.logger.info(f"Testing access to presentation: {presentation_id}")
        # ... rest of method
```

### Performance Monitoring

```python
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@measure_time
def test_presentation_access(self, presentation_id):
    # ... existing code
```

## 🚀 Deployment

### Distribution

1. **Create setup.py**
   ```python
   from setuptools import setup, find_packages
   
   setup(
       name="google-slides-permission-checker",
       version="1.0.0",
       packages=find_packages(),
       install_requires=[
           "google-api-python-client>=2.0.0",
           "google-auth-httplib2>=0.1.0",
           "google-auth-oauthlib>=0.4.0",
       ],
       entry_points={
           "console_scripts": [
               "slides-checker=main:main",
           ],
       },
   )
   ```

2. **Create executable**
   ```bash
   # Using PyInstaller
   pip install pyinstaller
   pyinstaller --onefile main.py
   ```

### Docker Support

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]
```

## 🔄 Dependency Management

### Update Dependencies

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade google-api-python-client

# Update all packages
pip install --upgrade -r requirements.txt
```

### Security Audits

```bash
# Install safety for security audits
pip install safety

# Check for known vulnerabilities
safety check

# Update requirements.txt with security fixes
pip install --upgrade --force-reinstall -r requirements.txt
```

## 📈 Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def extract_presentation_id(self, url):
    # ... existing code
```

### Batch Processing

```python
def batch_test_presentations(self, presentation_ids):
    """Test multiple presentations efficiently"""
    results = {}
    for presentation_id in presentation_ids:
        success, presentation = self.test_presentation_access(presentation_id)
        results[presentation_id] = {
            'success': success,
            'presentation': presentation
        }
    return results
```

## 🧹 Code Quality

### Linting

```bash
# Install linting tools
pip install flake8 black isort

# Run linting
flake8 main.py
black main.py
isort main.py
```

### Type Hints

```python
from typing import Optional, Tuple, Dict, Any

def extract_presentation_id(self, url: str) -> Optional[str]:
    """Extract presentation ID from Google Slides URL"""
    # ... existing code

def test_presentation_access(self, presentation_id: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Test if we can access the presentation"""
    # ... existing code
```

## 📚 Documentation Updates

### Code Documentation

```python
def test_presentation_access(self, presentation_id: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Test if we can access the presentation.
    
    Args:
        presentation_id (str): The Google Slides presentation ID
        
    Returns:
        Tuple[bool, Optional[Dict]]: (success, presentation_data)
        
    Raises:
        HttpError: When API request fails
    """
    # ... existing code
```

### API Documentation

Keep API documentation updated with:
- Method signatures
- Parameter descriptions
- Return value descriptions
- Example usage
- Error handling

---

This maintenance guide should be updated as the project evolves. Regular reviews and updates ensure the codebase remains maintainable and secure. 