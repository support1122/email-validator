#!/usr/bin/env python3
"""
Email Validator using Kickbox API
This script validates a list of emails and provides a deliverable report of valid emails.
"""

import requests
import time
import json
from typing import List, Dict, Tuple
import os
from datetime import datetime

class EmailValidator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.kickbox.com/v2/verify"
        self.deliverable_emails = []
        self.undeliverable_emails = []
        
    def validate_email(self, email: str) -> Dict:
        """
        Validate a single email using Kickbox API
        """
        params = {
            'email': email,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'email': email}
    
    def process_emails(self, emails: List[str], delay: float = 0.1) -> None:
        """
        Process a list of emails with rate limiting
        """
        total_emails = len(emails)
        print(f"Starting validation of {total_emails} emails...")
        print("=" * 50)
        
        for i, email in enumerate(emails, 1):
            print(f"Processing {i}/{total_emails}: {email}")
            
            result = self.validate_email(email)
            
            if 'error' in result:
                self.undeliverable_emails.append({'email': email, 'reason': f"API Error: {result['error']}"})
                print(f"  ❌ Undeliverable: {email} - API Error")
            else:
                deliverable = result.get('result', '')
                reason = result.get('reason', '')
                
                if deliverable == 'deliverable':
                    self.deliverable_emails.append(email)
                    print(f"  ✅ Deliverable: {email}")
                else:
                    # All other results (undeliverable, risky, unknown) go to undeliverable
                    self.undeliverable_emails.append({'email': email, 'reason': reason or deliverable})
                    print(f"  ❌ Undeliverable: {email} - {reason or deliverable}")
            
            # Rate limiting - Kickbox allows 100 requests per minute
            if i < total_emails:
                time.sleep(delay)
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive report of the validation results
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
EMAIL VALIDATION REPORT
Generated: {timestamp}
API: Kickbox

SUMMARY:
- Total emails processed: {len(self.deliverable_emails) + len(self.undeliverable_emails)}
- Deliverable emails: {len(self.deliverable_emails)}
- Undeliverable emails: {len(self.undeliverable_emails)}

DELIVERABLE EMAILS:
{chr(10).join(self.deliverable_emails) if self.deliverable_emails else "None"}

UNDELIVERABLE EMAILS:
"""
        
        for item in self.undeliverable_emails:
            report += f"- {item['email']}: {item['reason']}\n"
        
        return report
    
    def save_deliverable_emails(self, filename: str = "deliverable_emails.txt") -> None:
        """
        Save only the deliverable emails to a file
        """
        with open(filename, 'w') as f:
            for email in self.deliverable_emails:
                f.write(f"{email}\n")
        print(f"\n✅ Deliverable emails saved to: {filename}")


def main():
    # Kickbox API key from environment
    API_KEY = os.environ.get("KICKBOX_API_KEY", "")
    if not API_KEY:
        raise RuntimeError("KICKBOX_API_KEY environment variable is required")
    
    # Email list
    # Accept emails from a file path or stdin to avoid hardcoding
    emails_env_path = os.environ.get("EMAILS_FILE")
    emails: List[str] = []
    if emails_env_path and os.path.exists(emails_env_path):
        with open(emails_env_path, 'r') as f:
            emails = [line.strip() for line in f if line.strip()]
    else:
        print("Provide emails via EMAILS_FILE env var pointing to a file with one email per line.")
        return
    
    # Initialize validator
    validator = EmailValidator(API_KEY)
    
    # Process emails
    validator.process_emails(emails, delay=0.6)  # 0.6 second delay to respect rate limits
    
    # Generate and save report
    report = validator.generate_report()
    print(report)
    
    # Save report to file
    with open("email_validation_report.txt", "w") as f:
        f.write(report)
    
    # Save deliverable emails
    validator.save_deliverable_emails()
    
    print(f"\n📊 Final Results:")
    print(f"✅ Deliverable emails: {len(validator.deliverable_emails)}")
    print(f"❌ Undeliverable emails: {len(validator.undeliverable_emails)}")


if __name__ == "__main__":
    main()
