# Email Validator Web Application

A professional web interface for email validation using the Kickbox API. This application provides a modern, responsive UI for validating email addresses and downloading results in CSV format.

## Features

- 🌐 **Modern Web Interface**: Clean, professional design with Bootstrap 5
- 📧 **Bulk Email Validation**: Paste multiple emails and validate them all at once
- 📊 **Real-time Results**: See validation results as they're processed
- 📁 **CSV Downloads**: Download deliverable and undeliverable emails separately
- 📋 **Copy to Clipboard**: Copy individual emails with one click
- 📈 **Statistics Dashboard**: View validation statistics at a glance
- ⚡ **Rate Limiting**: Respects Kickbox API rate limits (100 requests/minute)

## Quick Start

### Option 1: Using the Launcher Script (Recommended)
```bash
python run_app.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at: **http://localhost:5000**

## How to Use

1. **Open the Web Interface**: Navigate to `http://localhost:5000` in your browser
2. **Paste Emails**: Copy and paste your email list into the text area (one email per line)
3. **Validate**: Click the "Validate Emails" button
4. **View Results**: See deliverable and undeliverable emails in separate sections
5. **Download**: Use the download buttons to get CSV files
6. **Copy**: Click the copy button next to any email to copy it to clipboard

## API Endpoints

- `GET /` - Main web interface
- `POST /validate` - Validate email list (JSON: `{"emails": "email1@example.com\nemail2@example.com"}`)
- `GET /download/deliverable` - Download deliverable emails as CSV
- `GET /download/undeliverable` - Download undeliverable emails as CSV

## File Structure

```
python-script-kickbox/
├── app.py                 # Main Flask application
├── run_app.py            # Application launcher script
├── templates/
│   └── index.html        # Web interface template
├── requirements.txt      # Python dependencies
├── email_validator.py    # Original CLI version
└── README_WEB.md        # This file
```

## Features in Detail

### Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Gradient backgrounds, smooth animations, and professional styling
- **Loading States**: Visual feedback during email validation
- **Error Handling**: Clear error messages and validation feedback

### Email Validation
- **Bulk Processing**: Validate hundreds of emails at once
- **Rate Limiting**: Automatic delays to respect API limits
- **Error Handling**: Graceful handling of API errors and network issues
- **Real-time Updates**: See results as they're processed

### Results Management
- **Separate Lists**: Deliverable and undeliverable emails shown separately
- **Detailed Information**: Reasons for undeliverable emails
- **CSV Export**: Download results in spreadsheet format
- **Copy Functionality**: Copy individual emails to clipboard

### Statistics
- **Total Processed**: Number of emails validated
- **Deliverable Count**: Number of valid emails
- **Undeliverable Count**: Number of invalid emails
- **Visual Indicators**: Color-coded statistics

## Configuration

The application uses the Kickbox API key from the original script. To change the API key, edit the `API_KEY` variable in `app.py`.

## Dependencies

- **Flask**: Web framework
- **Requests**: HTTP library for API calls
- **Bootstrap 5**: Frontend CSS framework
- **Font Awesome**: Icons

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Common Issues

1. **Port 5000 in use**: Change the port in `app.py` (line: `app.run(port=5001)`)
2. **API Key issues**: Verify your Kickbox API key is valid
3. **Network errors**: Check your internet connection
4. **Rate limiting**: The app automatically handles rate limits, but very large lists may take time

### Getting Help

If you encounter issues:
1. Check the terminal output for error messages
2. Verify your Python environment and dependencies
3. Ensure your Kickbox API key is valid and has sufficient credits

## Security Notes

- The API key is embedded in the application for simplicity
- For production use, consider using environment variables
- The application runs on localhost by default for security

## Performance

- **Rate Limiting**: 0.6 second delay between API calls (100 requests/minute)
- **Memory Efficient**: Processes emails in batches
- **Responsive**: UI updates in real-time during processing

---

**Enjoy validating your emails with this professional web interface!** 🚀
