# Email Validator using Kickbox API

This Python script validates a list of emails using the Kickbox API and provides a deliverable report of valid emails.

## Features

- ✅ Validates emails using Kickbox API
- 📊 Generates comprehensive validation report
- 🚀 Rate limiting to respect API limits
- 📁 Saves valid emails to separate file
- ⚠️ Handles errors and risky emails
- 📈 Real-time progress tracking

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment and run:
```bash
# 1) Set Kickbox API key
export KICKBOX_API_KEY=your_kickbox_api_key

# 2a) Run web app (PORT optional, defaults to 5000)
export PORT=5001
python run_app.py

# 2b) Run CLI validator
export EMAILS_FILE=path/to/emails.txt   # one email per line
python email_validator.py
```

## Output Files

- `email_validation_report.txt` - Complete validation report
- `deliverable_emails.txt` - List of valid emails only

## API Rate Limits

The script includes a 0.6-second delay between API calls to respect Kickbox's rate limits (100 requests per minute).

## Email Categories

- **Deliverable**: Valid emails that can receive messages
- **Undeliverable**: Invalid emails, risky emails, or emails that couldn't be validated
