#!/usr/bin/env python3
"""
Email Validator Web Application using Kickbox API
A professional web interface for email validation
"""

from flask import Flask, render_template, request, jsonify, send_file, Response
import requests
import time
import json
import csv
import io
from typing import List, Dict
from datetime import datetime
import os

app = Flask(__name__)

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
    
    def process_emails(self, emails: List[str], delay: float = 0.1) -> Dict:
        """
        Process a list of emails with rate limiting
        """
        self.deliverable_emails = []
        self.undeliverable_emails = []
        
        total_emails = len(emails)
        results = {
            'deliverable': [],
            'undeliverable': [],
            'total_processed': 0,
            'errors': []
        }
        
        for i, email in enumerate(emails, 1):
            email = email.strip()
            if not email:
                continue
                
            result = self.validate_email(email)
            results['total_processed'] += 1
            
            if 'error' in result:
                error_info = {'email': email, 'reason': f"API Error: {result['error']}"}
                self.undeliverable_emails.append(error_info)
                results['undeliverable'].append(error_info)
                results['errors'].append(f"Error validating {email}: {result['error']}")
            else:
                deliverable = result.get('result', '')
                reason = result.get('reason', '')
                
                if deliverable == 'deliverable':
                    self.deliverable_emails.append(email)
                    results['deliverable'].append(email)
                else:
                    # All other results (undeliverable, risky, unknown) go to undeliverable
                    undeliverable_info = {'email': email, 'reason': reason or deliverable}
                    self.undeliverable_emails.append(undeliverable_info)
                    results['undeliverable'].append(undeliverable_info)
            
            # Rate limiting - Kickbox allows 100 requests per minute
            if i < total_emails:
                time.sleep(delay)
        
        return results

# Initialize validator with API key from environment
# Do not fail at import time; endpoints will validate presence and respond with clear error
API_KEY = os.environ.get("KICKBOX_API_KEY", "")
validator = EmailValidator(API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate_emails():
    try:
        if not validator.api_key:
            return jsonify({'error': 'KICKBOX_API_KEY not configured on server'}), 500
        data = request.get_json()
        emails_text = data.get('emails', '')
        
        if not emails_text.strip():
            return jsonify({'error': 'No emails provided'}), 400
        
        # Parse emails from text input
        emails = [email.strip() for email in emails_text.split('\n') if email.strip()]
        
        if not emails:
            return jsonify({'error': 'No valid emails found'}), 400
        
        # Process emails with faster rate limiting
        results = validator.process_emails(emails, delay=0.1)
        
        return jsonify({
            'success': True,
            'results': results,
            'deliverable_count': len(results['deliverable']),
            'undeliverable_count': len(results['undeliverable']),
            'total_processed': results['total_processed']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/validate_stream', methods=['POST'])
def validate_emails_stream():
    # Get data from request before entering the generator
    data = request.get_json()
    emails_text = data.get('emails', '')
    
    def generate():
        try:
            if not validator.api_key:
                yield f"data: {json.dumps({'type': 'error', 'error': 'KICKBOX_API_KEY not configured on server'})}\n\n"
                return
            if not emails_text.strip():
                yield f"data: {json.dumps({'error': 'No emails provided'})}\n\n"
                return
            
            # Parse emails from text input
            emails = [email.strip() for email in emails_text.split('\n') if email.strip()]
            
            if not emails:
                yield f"data: {json.dumps({'error': 'No valid emails found'})}\n\n"
                return
            
            # Initialize results
            deliverable_emails = []
            undeliverable_emails = []
            total_emails = len(emails)
            
            # Send initial progress
            yield f"data: {json.dumps({'type': 'progress', 'current': 0, 'total': total_emails, 'percentage': 0})}\n\n"
            
            # Process emails with faster rate limiting
            for i, email in enumerate(emails, 1):
                result = validator.validate_email(email)
                
                if 'error' in result:
                    undeliverable_emails.append({'email': email, 'reason': f"API Error: {result['error']}"})
                else:
                    deliverable = result.get('result', '')
                    reason = result.get('reason', '')
                    
                    if deliverable == 'deliverable':
                        deliverable_emails.append(email)
                    else:
                        undeliverable_emails.append({'email': email, 'reason': reason or deliverable})
                
                # Send progress update
                percentage = int((i / total_emails) * 100)
                yield f"data: {json.dumps({'type': 'progress', 'current': i, 'total': total_emails, 'percentage': percentage, 'current_email': email})}\n\n"
                
                # Rate limiting
                if i < total_emails:
                    time.sleep(0.1)
            
            # Send final results
            final_results = {
                'type': 'complete',
                'success': True,
                'results': {
                    'deliverable': deliverable_emails,
                    'undeliverable': undeliverable_emails,
                    'total_processed': total_emails
                },
                'deliverable_count': len(deliverable_emails),
                'undeliverable_count': len(undeliverable_emails),
                'total_processed': total_emails
            }
            yield f"data: {json.dumps(final_results)}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/download/deliverable')
def download_deliverable():
    try:
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Email'])
        
        for email in validator.deliverable_emails:
            writer.writerow([email])
        
        # Create BytesIO object for file download
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8'))
        mem.seek(0)
        
        filename = f"deliverable_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return send_file(
            mem,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/undeliverable')
def download_undeliverable():
    try:
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Email', 'Reason'])
        
        for item in validator.undeliverable_emails:
            writer.writerow([item['email'], item['reason']])
        
        # Create BytesIO object for file download
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8'))
        mem.seek(0)
        
        filename = f"undeliverable_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return send_file(
            mem,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    debug_flag = os.environ.get('FLASK_DEBUG', '0') in ('1', 'true', 'True')
    port = int(os.environ.get('PORT', '5000'))
    app.run(debug=debug_flag, host='0.0.0.0', port=port)
