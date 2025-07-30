# Google Slides API Permission Checker

A Python tool to test and verify access permissions for Google Slides presentations using the Google Slides API.

## 🌟 Features

- **OAuth Authentication**: Secure Google account authentication
- **Permission Testing**: Check if you can access specific Google Slides presentations
- **Content Extraction**: Extract text, images, and speaker notes from presentations
- **Interactive Mode**: User-friendly command-line interface
- **Error Handling**: Detailed error messages for different access scenarios
- **Export Capability**: Save extracted content to JSON files

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- Google account with access to Google Slides
- Google Cloud Project with Google Slides API enabled
- Virtual environment (recommended for isolation)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd Google-Slides-API-Permission-Checker
   ```

2. **Set up virtual environment (recommended)**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   
   # Verify activation (you should see (venv) in your terminal)
   ```

3. **Install required dependencies**
   ```bash
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
   
   **Alternative: Install from requirements.txt**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Enable the Google Slides API
   - Go to "Credentials" → "Create Credentials" → "OAuth client ID"
   - Choose "Desktop application"
   - Download the JSON file and rename it to `credentials.json`
   - Place the file in the same directory as `main.py`

5. **Run the application**
   ```bash
   python main.py
   ```

## 📖 Usage

### Basic Usage

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Follow the OAuth flow**
   - Your browser will open automatically
   - Log in to your Google account
   - Authorize the application to access your Google Slides

3. **Test presentation access**
   - Enter a Google Slides URL or presentation ID
   - The tool will check if you have permission to access it
   - View basic information about the presentation

4. **Extract content (optional)**
   - Choose whether to extract full content
   - Content will be saved to a JSON file

### Supported URL Formats

- Full Google Slides URL: `https://docs.google.com/presentation/d/PRESENTATION_ID/edit`
- Presentation ID only: `PRESENTATION_ID`

### Example Output

```
🔍 Testing access to presentation: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
✅ Successfully accessed presentation!
   📋 Title: Sample Presentation
   📊 Slides: 5

📝 Sample content extraction:
   🎯 First slide (ID: slide_1):
      📄 Text: Welcome to our presentation...
   🖼️  Total images: 3
   🗣️  Slides with notes: 2
```

## 🔧 Configuration

### OAuth Scopes

The application uses read-only scope:
```
https://www.googleapis.com/auth/presentations.readonly
```

### Files

- `main.py`: Main application file
- `credentials.json`: Google OAuth credentials (you need to create this)
- `token.json`: Generated automatically after first authentication
- `slides_content_*.json`: Exported content files
- `venv/`: Virtual environment directory (created during setup)
- `requirements.txt`: Python dependencies list

## 🛠️ Troubleshooting

### Common Issues

1. **"Missing Google API libraries"**
   ```bash
   # Make sure your virtual environment is activated
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

2. **"File 'credentials.json' not found"**
   - Follow the setup instructions above to create credentials.json
   - Make sure the file is in the same directory as main.py
   - Ensure you're running the script from the correct directory

3. **"Access denied (403)"**
   - The presentation is private or you don't have permission
   - Ask the owner to share the presentation with your Google account

4. **"Presentation not found (404)"**
   - Check the URL or presentation ID
   - The presentation may have been deleted

### Error Codes

- **403**: Access denied - no permission to view
- **404**: Presentation not found - incorrect ID or deleted
- **401**: Authentication failed - re-run OAuth flow

## 📊 Output Format

When extracting full content, the tool creates a JSON file with this structure:

```json
{
  "presentation_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
  "title": "Sample Presentation",
  "slides": [
    {
      "slide_number": 1,
      "slide_id": "slide_1",
      "text_content": [
        {
          "object_id": "text_1",
          "text": "Welcome to our presentation"
        }
      ],
      "speaker_notes": "Additional notes for this slide",
      "images": [
        {
          "object_id": "image_1",
          "content_url": "https://..."
        }
      ],
      "shapes": []
    }
  ]
}
```

## 🔒 Security

- OAuth tokens are stored locally in `token.json`
- Only read-only permissions are requested
- No data is sent to external servers
- Credentials are stored securely using Google's OAuth library

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your Google Cloud setup
3. Ensure you have the correct permissions for the presentation
4. Check that the Google Slides API is enabled in your project

---

**Note**: This tool is for testing and educational purposes. Always respect the privacy and permissions of Google Slides presentations. 