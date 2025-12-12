# AERO - Airport Surveillance System

A comprehensive facial recognition surveillance system designed for airport security. Real-time face detection, matching, and alerts with a modern dashboard UI.

## Features

✅ **Multi-Camera Support** - Manage multiple camera streams simultaneously  
✅ **Real-Time Face Recognition** - Compare faces against database using embeddings  
✅ **Security Alerts** - HIGH/YELLOW severity alerts with timestamps  
✅ **Live Streaming** - MJPEG streams with bounding boxes for detected faces  
✅ **Suspicious Person Upload** - Upload images to match against database  
✅ **Control Panel** - Confidence threshold adjustment and camera status  
✅ **Error Handling** - Comprehensive error logging and recovery  
✅ **Environment Configuration** - Easy setup with environment variables  

---

## Project Structure

```
AERO/
├── Backend/
│   ├── app.py                 # Flask server (Python fullstack)
│   ├── camera_manager.py      # Camera stream handling
│   ├── face_utils.py          # Face recognition logic
│   ├── setup.py               # Embedding generation utility
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── templates/
│   │   └── index.html         # Dashboard UI (Jinja2)
│   ├── static/
│   │   ├── style.css          # Modern dark theme CSS
│   │   └── script.js          # Client-side JavaScript
│   └── Data/                  # (excluded from git)
│       ├── Images/            # Face images for database
│       ├── profile.xlsx       # Profile data
│       └── embeddings.pkl     # Generated embeddings
│
└── README.md                  # This file
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, Vanilla JavaScript, CSS3 |
| **Backend** | Flask, OpenCV, face_recognition |
| **Templates** | Jinja2 (server-side rendering) |
| **Database** | Pickle (embeddings), Excel (profiles) |
| **Architecture** | Python-only fullstack (no npm/Node.js) |

---

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Backend Setup

1. Navigate to Backend directory:
```bash
cd Backend
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables (`.env`):
```env
FLASK_ENV=development
DEBUG=True
LOG_LEVEL=INFO
```

5. Generate embeddings (if you have data):
```bash
python setup.py
```

---

## Running the Application

### Start the Flask Server

```bash
cd Backend
python app.py
```

The application will be available at: **`http://127.0.0.1:5000`**

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Accessing the Dashboard

Open your browser to `http://127.0.0.1:5000` to access the surveillance dashboard with:
- Live camera feeds
- Real-time alerts
- Suspicious person upload
- System status monitoring

---

## API Endpoints

### Cameras

**GET** `/api/cameras`
- List all available cameras
- Response: `{"cameras": ["cam1", "cam2", ...]}`

**GET** `/api/stream/<cam_id>`
- Stream live video from camera with face detection overlays
- Returns MJPEG stream (display with `<img src="/api/stream/cam1">`)

### Face Recognition

**POST** `/api/upload_suspicious`
- Upload image to match against database
- Body: FormData with `file` (image)
- Response: `{"matches": [{"urn": "...", "distance": 0.45, ...}]}`

### Health & Status

**GET** `/api/health`
- Health check endpoint
- Response: `{"status": "running", "message": "..."}`

**GET** `/api/status`
- Get system status (cameras, embeddings loaded, etc.)
- Response: `{"cameras": 1, "embeddings_loaded": true, ...}`

### Dashboard

**GET** `/`
- Renders the main surveillance dashboard (index.html)

---

## Environment Variables

### Backend (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Flask environment mode |
| `DEBUG` | `True` | Enable debug mode (disable in production) |
| `LOG_LEVEL` | `INFO` | Logging level (INFO, DEBUG, WARNING) |

---

## Database Setup

### Profile Excel Format

Your `profile.xlsx` should have these columns:

| Column | Description |
|--------|-------------|
| URN | Unique identifier |
| Image Address | Relative path to image (e.g., `person_001.jpg`) |
| (Other columns) | Additional profile data |

### Generating Embeddings

1. Prepare your data:
   - Place images in `Backend/Data/Images/`
   - Create `Backend/Data/profile.xlsx` with image paths

2. Run setup script:
```bash
cd Backend
python setup.py
```

This generates `Backend/Data/embeddings.pkl` containing face embeddings and profile details.

---

## Error Handling

The application includes comprehensive error handling:

- **API Errors**: All endpoints return proper HTTP status codes and error messages
- **Logging**: All operations logged to console/files with different levels (INFO, WARNING, ERROR)
- **Frame Processing**: Graceful degradation if frames are missing or invalid
- **File Handling**: Safe file loading with fallbacks

Check logs for debugging:
- Backend: Console output from `uvicorn app:app --reload`
- Frontend: Browser console (F12)

---

## Configuration

### Confidence Threshold

Adjust face matching confidence in the UI (default: 0.6):
- Lower = More matches (less strict)
- Higher = Fewer matches (more strict)

Edit in `SurveillanceControl.jsx` or make it dynamic via API.

### Adding Cameras

Edit `Backend/app.py` `CAMERAS` dictionary:

```python
CAMERAS = {
    "cam1": CameraStream(0, "cam1"),           # Webcam
    "cam2": CameraStream("rtsp://...", "cam2"), # RTSP stream
    "cam3": CameraStream("video.mp4", "cam3"),  # Video file
}
```

---

## Security Notes

⚠️ **Current State**: This is development code  
✓ **To Deploy to Production**:

1. Add authentication (JWT, OAuth2)
2. Use HTTPS/TLS
3. Add rate limiting
4. Validate all file uploads
5. Use secure database (PostgreSQL instead of pickle)
6. Add audit logging
7. Implement access controls
8. Use secrets management for credentials

---

## Troubleshooting

### Backend won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process (Windows)
taskkill /PID <PID> /F
```

### Camera not working
- Check camera permissions
- Verify camera is connected: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`

### No embeddings loaded
- Ensure `embeddings.pkl` exists in `Backend/Data/`
- Run `python Backend/setup.py` to generate
- System will continue to work without embeddings (no face matching)

### Frontend can't reach backend
- Verify backend is running on port 5000
- Check browser console (F12) for network errors
- Ensure Flask CORS is configured correctly

---

## Production Deployment

### Using Gunicorn (Recommended)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run Flask app with Gunicorn:
```bash
cd Backend
gunicorn --workers=4 --bind=0.0.0.0:5000 app:app
```

### Using uWSGI

```bash
pip install uwsgi
uwsgi --http=:5000 --wsgi-file=app.py --callable=app --processes=4 --threads=2
```

### Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/TLS with reverse proxy (nginx/Apache)
- [ ] Add authentication (JWT, OAuth2)
- [ ] Implement rate limiting
- [ ] Add audit logging
- [ ] Validate all file uploads
- [ ] Use a proper database (PostgreSQL) instead of pickle
- [ ] Set up CORS restrictions properly

---

## Git Setup

The project is configured to exclude data folder:

```bash
# Push to GitHub (data/ excluded)
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

## Future Enhancements

- [ ] Real-time database (PostgreSQL)
- [ ] Advanced alert system (email, SMS)
- [ ] Multi-user support with roles
- [ ] Video recording and playback
- [ ] Advanced analytics dashboard
- [ ] Mobile app
- [ ] Cloud deployment (AWS/Azure)

---

## License

This project is part of AERO surveillance system.

---

## Support

For issues or questions, refer to logs or contact the development team.
