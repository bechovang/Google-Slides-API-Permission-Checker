#!/usr/bin/env python3
"""
Google Slides API Permission Checker
Kiểm tra quyền truy cập và test Google Slides API
"""

import os
import sys
import re
from pathlib import Path
import json
from urllib.parse import urlparse, parse_qs

# Google API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    print("✅ Google API libraries imported successfully")
except ImportError as e:
    print("❌ Missing Google API libraries!")
    print("Run: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

# Scopes - chỉ cần read-only
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']

class GoogleSlidesChecker:
    def __init__(self):
        self.creds = None
        self.service = None
        self.credentials_file = "credentials.json"
        self.token_file = "token.json"
    
    def setup_credentials(self):
        """Setup OAuth credentials"""
        print("\n🔐 Setting up Google OAuth credentials...")
        
        # Check if credentials.json exists
        if not os.path.exists(self.credentials_file):
            print(f"❌ File '{self.credentials_file}' not found!")
            print("\n📋 To create credentials.json:")
            print("1. Go to: https://console.cloud.google.com")
            print("2. Create a new project or select existing one")
            print("3. Enable Google Slides API")
            print("4. Go to 'Credentials' → 'Create Credentials' → 'OAuth client ID'")
            print("5. Choose 'Desktop application'")
            print("6. Download the JSON file and rename it to 'credentials.json'")
            print("7. Put the file in the same folder as this script")
            return False
        
        # Load existing token
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If no valid credentials, run OAuth flow
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("🔄 Refreshing expired token...")
                self.creds.refresh(Request())
            else:
                print("🌐 Starting OAuth flow...")
                print("Your browser will open. Please login and authorize the app.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save credentials for next time
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())
            print("✅ Credentials saved!")
        
        return True
    
    def build_service(self):
        """Build Google Slides service"""
        try:
            self.service = build('slides', 'v1', credentials=self.creds)
            print("✅ Google Slides service initialized")
            return True
        except Exception as e:
            print(f"❌ Failed to build service: {e}")
            return False
    
    def extract_presentation_id(self, url):
        """Extract presentation ID from Google Slides URL"""
        patterns = [
            r'/presentation/d/([a-zA-Z0-9-_]+)',
            r'id=([a-zA-Z0-9-_]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # If it's already just an ID
        if re.match(r'^[a-zA-Z0-9-_]+$', url):
            return url
        
        return None
    
    def test_presentation_access(self, presentation_id):
        """Test if we can access the presentation"""
        print(f"\n🔍 Testing access to presentation: {presentation_id}")
        
        try:
            # Try to get basic presentation info
            presentation = self.service.presentations().get(
                presentationId=presentation_id
            ).execute()
            
            title = presentation.get('title', 'Untitled')
            slide_count = len(presentation.get('slides', []))
            
            print(f"✅ Successfully accessed presentation!")
            print(f"   📋 Title: {title}")
            print(f"   📊 Slides: {slide_count}")
            
            return True, presentation
            
        except HttpError as e:
            error_code = e.resp.status
            if error_code == 403:
                print("❌ Access denied (403)")
                print("   Possible reasons:")
                print("   - No permission to view this presentation")
                print("   - Presentation is private")
                print("   - Need to be shared with your Google account")
            elif error_code == 404:
                print("❌ Presentation not found (404)")
                print("   Possible reasons:")
                print("   - Incorrect presentation ID")
                print("   - Presentation was deleted")
                print("   - URL is malformed")
            else:
                print(f"❌ HTTP Error {error_code}: {e}")
            
            return False, None
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False, None
    
    def extract_sample_content(self, presentation):
        """Extract and display sample content"""
        print("\n📝 Sample content extraction:")
        
        slides = presentation.get('slides', [])
        if not slides:
            print("   No slides found")
            return
        
        # Show first slide content
        first_slide = slides[0]
        print(f"   🎯 First slide (ID: {first_slide['objectId']}):")
        
        text_found = False
        for element in first_slide.get('pageElements', []):
            if 'shape' in element and 'text' in element['shape']:
                text_elements = element['shape']['text']['textElements']
                text = ''.join(
                    run.get('textRun', {}).get('content', '')
                    for run in text_elements
                ).strip()
                
                if text:
                    # Show first 100 characters
                    preview = text[:100] + "..." if len(text) > 100 else text
                    print(f"      📄 Text: {preview}")
                    text_found = True
                    break
        
        if not text_found:
            print("      📄 No text content found in first slide")
        
        # Check for images
        image_count = sum(
            1 for slide in slides
            for element in slide.get('pageElements', [])
            if 'image' in element
        )
        print(f"   🖼️  Total images: {image_count}")
        
        # Check for speaker notes
        notes_count = sum(
            1 for slide in slides
            if slide.get('notesPage', {}).get('pageElements')
        )
        print(f"   🗣️  Slides with notes: {notes_count}")
    
    def run_interactive_test(self):
        """Run interactive testing session"""
        print("🚀 Google Slides API Permission Checker")
        print("=" * 50)
        
        # Step 1: Setup credentials
        if not self.setup_credentials():
            return
        
        # Step 2: Build service
        if not self.build_service():
            return
        
        print("\n✅ Setup complete! Ready to test presentations.")
        
        # Step 3: Interactive testing
        while True:
            print("\n" + "="*50)
            url_or_id = input("📎 Enter Google Slides URL or Presentation ID (or 'quit' to exit): ").strip()
            
            if url_or_id.lower() in ['quit', 'exit', 'q']:
                break
            
            if not url_or_id:
                continue
            
            # Extract presentation ID
            presentation_id = self.extract_presentation_id(url_or_id)
            if not presentation_id:
                print("❌ Invalid URL or ID format")
                print("Expected formats:")
                print("  - https://docs.google.com/presentation/d/PRESENTATION_ID/edit")
                print("  - Just the PRESENTATION_ID")
                continue
            
            # Test access
            success, presentation = self.test_presentation_access(presentation_id)
            
            if success:
                self.extract_sample_content(presentation)
                
                # Ask if user wants full extraction
                extract = input("\n🤔 Do you want to extract full content? (y/n): ").strip().lower()
                if extract in ['y', 'yes']:
                    self.full_content_extraction(presentation_id, presentation)
        
        print("\n👋 Thanks for using Google Slides API Checker!")
    
    def full_content_extraction(self, presentation_id, presentation):
        """Extract full content and save to file"""
        print("\n📊 Extracting full content...")
        
        extracted_data = {
            'presentation_id': presentation_id,
            'title': presentation.get('title', 'Untitled'),
            'slides': []
        }
        
        for i, slide in enumerate(presentation.get('slides', [])):
            slide_data = {
                'slide_number': i + 1,
                'slide_id': slide['objectId'],
                'text_content': [],
                'speaker_notes': '',
                'images': [],
                'shapes': []
            }
            
            # Extract text from shapes
            for element in slide.get('pageElements', []):
                if 'shape' in element and 'text' in element['shape']:
                    text_elements = element['shape']['text']['textElements']
                    text = ''.join(
                        run.get('textRun', {}).get('content', '')
                        for run in text_elements
                    ).strip()
                    
                    if text:
                        slide_data['text_content'].append({
                            'object_id': element['objectId'],
                            'text': text
                        })
                
                # Extract images
                if 'image' in element:
                    slide_data['images'].append({
                        'object_id': element['objectId'],
                        'content_url': element['image']['contentUrl']
                    })
            
            # Extract speaker notes
            notes_page = slide.get('notesPage', {})
            for element in notes_page.get('pageElements', []):
                if 'shape' in element and 'text' in element['shape']:
                    notes_elements = element['shape']['text']['textElements']
                    notes = ''.join(
                        run.get('textRun', {}).get('content', '')
                        for run in notes_elements
                    ).strip()
                    
                    if notes and 'Click to add speaker notes' not in notes:
                        slide_data['speaker_notes'] = notes
            
            extracted_data['slides'].append(slide_data)
        
        # Save to file
        output_file = f"slides_content_{presentation_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Full content saved to: {output_file}")
        
        # Show summary
        total_text_blocks = sum(len(slide['text_content']) for slide in extracted_data['slides'])
        total_images = sum(len(slide['images']) for slide in extracted_data['slides'])
        slides_with_notes = sum(1 for slide in extracted_data['slides'] if slide['speaker_notes'])
        
        print(f"📊 Extraction Summary:")
        print(f"   📄 Total slides: {len(extracted_data['slides'])}")
        print(f"   📝 Text blocks: {total_text_blocks}")
        print(f"   🖼️  Images: {total_images}")
        print(f"   🗣️  Slides with notes: {slides_with_notes}")

def main():
    checker = GoogleSlidesChecker()
    checker.run_interactive_test()

if __name__ == "__main__":
    main()