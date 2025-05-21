# Indurkar Dental Clinic QR Code System

This application generates a QR code for Indurkar Dental Clinic's location and provides a feedback system for patients.

## Features

- QR code generation for clinic location
- Feedback form for patient reviews
- Star rating system
- Database storage for feedback

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. The main page displays a QR code that links to the clinic's Google Maps location
2. When scanned, the QR code will open Google Maps with the clinic's location
3. Users can provide feedback by filling out the feedback form
4. Feedback is stored in a SQLite database (`feedback.db`)

## Database

The application uses SQLite to store feedback. The database file (`feedback.db`) will be created automatically when you first run the application.

## Security Note

Before deploying to production:
1. Change the `SECRET_KEY` in `app.py`
2. Use a production-grade database
3. Implement proper security measures 