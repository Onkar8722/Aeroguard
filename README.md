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
│   ├── app.py                 # FastAPI server
│   ├── camera_manager.py      # Camera stream handling
│   ├── face_utils.py          # Face recognition logic
│   ├── setup.py               # Embedding generation utility
│   ├── .env                   # Environment variables
│   └── Data/                  # (excluded from git)
│       ├── Images/            # Face images for database
│       ├── profile.xlsx       # Profile data
│       └── embeddings.pkl     # Generated embeddings
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── api.js             # API client with error handling
│   │   ├── main.jsx           # React entry point
│   │   ├── index.css          # Tailwind styles
│   │   └── components/
│   │       ├── CameraFeed.jsx
│   │       ├── SecurityAlerts.jsx
│   │       ├── StatusCards.jsx
│   │       ├── SurveillanceControl.jsx
│   │       └── UploadBox.jsx
│   ├── .env                   # Frontend env variables
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md                  # This file
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Vite, Tailwind CSS |
| **Backend** | FastAPI, OpenCV, face_recognition |
| **Database** | Pickle (embeddings), Excel (profiles) |
| **Build Tools** | npm, Vite |

---

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to Backend directory:
```bash
cd Backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install fastapi uvicorn opencv-python face_recognition pandas openpyxl
```

4. Configure environment variables (`.env`):
```env
CORS_ORIGINS=http://localhost:5173
DATA_DIR=Backend/Data/Images
PROFILE_FILE=Backend/Data/profile.xlsx
EMBEDDINGS_PATH=Backend/Data/embeddings.pkl
LOG_LEVEL=INFO
```

5. Generate embeddings (if you have data):
```bash
python setup.py
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables (`.env`):
```env
VITE_API_URL=http://127.0.0.1:8000
```

---

## Running the Application

### Backend

```bash
cd Backend
uvicorn app:app --reload --port 8000
```

Backend will be available at: `http://127.0.0.1:8000`

### Frontend

In a new terminal:

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:5173`

---

## API Endpoints

### Cameras

**GET** `/cameras`
- List all available cameras
- Response: `{"cameras": ["cam1", "cam2", ...]}`

**GET** `/stream/{cam_id}`
- Stream live video from camera with face detection overlays
- Returns MJPEG stream

### Face Recognition

**POST** `/upload_suspicious`
- Upload image to match against database
- Body: FormData with `file` (image)
- Response: `{"matches": [{"urn": "...", "distance": 0.45, ...}]}`

### Health

**GET** `/`
- Health check endpoint
- Response: `{"status": "running", "message": "..."}`

---

## Environment Variables

### Backend (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated CORS allowed origins |
| `DATA_DIR` | `Backend/Data/Images` | Directory containing face images |
| `PROFILE_FILE` | `Backend/Data/profile.xlsx` | Excel file with profile data |
| `EMBEDDINGS_PATH` | `Backend/Data/embeddings.pkl` | Path to embeddings database |
| `LOG_LEVEL` | `INFO` | Logging level |

### Frontend (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://127.0.0.1:8000` | Backend API URL |

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
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

### Camera not working
- Check camera permissions
- Verify camera is connected: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`

### No embeddings loaded
- Ensure `embeddings.pkl` exists in `Backend/Data/`
- Run `python Backend/setup.py` to generate

### Frontend can't reach backend
- Verify backend is running on port 8000
- Check `VITE_API_URL` in `.env`
- Check CORS settings in `Backend/.env`

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
