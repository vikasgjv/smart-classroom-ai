# 🎓 ClassAI - Smart Classroom Attention Monitoring System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

ClassAI is an AI-powered real-time classroom monitoring system that tracks student attention and engagement using computer vision and facial recognition technology.

## ✨ Features

### 🎯 Core Features
- **Real-Time Attention Monitoring** - Continuous webcam-based attention tracking
- **Face Detection** - Advanced OpenCV-based face and eye detection
- **Engagement Analysis** - Color-coded attention levels (Green/Orange/Red)
- **Absence Tracking** - Automatic detection when student is not present
- **Session Reports** - Comprehensive analytics and performance reports

### 🌟 Advanced Features
- **🌙 Dark Mode** - Eye-friendly interface for evening classes
- **📄 PDF Export** - One-click report export for easy sharing
- **⚠️ Absence Alerts** - Real-time notifications after 2 minutes of absence
- **📊 Live Charts** - Interactive attention timeline visualization
- **💾 Database Storage** - SQLite-based data persistence

### 🎨 User Interface
- Modern, responsive card-based design
- Real-time attention circle with pulse animation
- Live statistics dashboard
- Smooth animations and transitions
- Mobile-friendly responsive layout

## 📸 Screenshots

### Dashboard (Light Mode)
![Dashboard Light Mode](screenshots/jpg.1)
*Clean, modern interface with real-time monitoring*

### Dashboard (Dark Mode)
![Dashboard Dark Mode](screenshots/jpg.2)
*Eye-friendly dark theme for evening classes*

### Live Monitoring
![Live Monitoring](screenshots/jpg.3)
*Real-time face detection and attention tracking*


## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ClassAI.git
cd ClassAI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
# Start backend server (Terminal 1)
python main.py

# Start frontend server (Terminal 2)
python -m http.server 3001
```

4. **Access the dashboard**
```
http://localhost:3001
```

## 📖 Usage

### Starting a Session
1. Open the dashboard in your browser
2. Click **"Start Class"** button
3. Allow webcam access when prompted
4. System begins monitoring automatically

### Monitoring Attention
- **Green (80%+)**: High attention/focus
- **Orange (50-79%)**: Medium attention
- **Red (<50%)**: Low attention/distracted
- **Gray**: No face detected (absent)

### Generating Reports
1. Click **"End Class"** when session is complete
2. Click **"Generate Report"** button
3. View detailed analytics
4. Click **"Export PDF"** to save report

### Using Dark Mode
- Click the moon/sun icon in the top-right corner
- Theme preference is saved automatically
- Perfect for evening or night classes

## 🏗 Architecture

```text
ClassAI/
├── backend/
│   ├── main.py                  # FastAPI backend server
│   ├── continuous_webcam.py     # Webcam monitoring & face detection
│   ├── database.py              # Database operations
│   ├── models.py                # Data models / schemas
│   └── report_generator.py      # Report generation logic
│
├── frontend/
│   ├── index.html               # Frontend dashboard
│   ├── script.js                # Frontend JavaScript logic
│   └── style.css                # Styling (dark mode UI)
│
├── models_ai/
│   └── haarcascade_frontalface_default.xml   # Face detection model
│
├── docs/
│   ├── FEATURES.md              # Project features
│   ├── SETUP.md                 # Setup instructions
│   ├── QUICKSTART.md            # Quick start guide
│   ├── PROJECT_STRUCTURE.md     # Architecture overview
│   └── CONTRIBUTING.md          # Contribution guidelines
│
├── screenshots/
│   └── dashboard.png            # UI screenshots (optional)
│
├── requirements.txt             # Python dependencies
├── README.md                    # Project overview
├── LICENSE
└── .gitignore



## 🔧 Configuration

### Absence Alert Threshold
Change the alert timing in `script.js`:
```javascript
const ABSENCE_ALERT_THRESHOLD = 2; // Minutes
```

### Attention Update Interval
Modify update frequency in `script.js`:
```javascript
updateInterval = setInterval(() => {
    updateAttentionMetrics();
}, 3000); // Milliseconds (3 seconds)
```

### Camera Settings
Adjust in `continuous_webcam.py`:
```python
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30
```

## 🌐 Network Deployment

### Local Network Setup
1. Find your computer's IP address:
```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig
```

2. Students connect to:
```
http://YOUR-IP:3001
```

### Cloud Deployment
Deploy to AWS, Google Cloud, or DigitalOcean:
1. Install dependencies on server
2. Update API URLs in `script.js`
3. Configure firewall for ports 3001 and 8001
4. Use reverse proxy (nginx) for production

## 📊 API Endpoints

### Start Monitoring
```http
POST /start-monitoring
```

### Stop Monitoring
```http
POST /stop-monitoring
```

### Get Live Attention
```http
POST /live-attention
Content-Type: application/json

{
  "student_id": "S01"
}
```

### Generate Report
```http
POST /generate-report
Content-Type: application/json

{
  "student_id": "S01",
  "session_start": "2026-02-07T10:00:00",
  "session_end": "2026-02-07T11:00:00"
}
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.8+
- **Computer Vision**: OpenCV 4.5+
- **Database**: SQLite with SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js
- **PDF Export**: html2pdf.js
- **Face Detection**: Haar Cascade Classifiers

## 🎯 Use Cases

- **Educational Institutions**: Monitor student engagement in classrooms
- **Online Learning**: Track attention during virtual classes
- **Corporate Training**: Measure trainee focus and participation
- **Research**: Study attention patterns and learning behaviors

## 🔒 Privacy & Security

- All data stored locally on your machine
- No data sent to external servers
- Webcam access only during active sessions
- Students can see what's being monitored
- GDPR and privacy-compliant design

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- Face detection may be affected by poor lighting
- Glasses/specs can sometimes reduce detection accuracy
- Requires stable webcam connection

## 🔮 Future Enhancements

- [ ] Multi-student monitoring (classroom view)
- [ ] WebSocket for real-time updates
- [ ] Emotion detection (happy, confused, bored)
- [ ] Hand raise detection
- [ ] Integration with LMS platforms
- [ ] Mobile app support
- [ ] Advanced analytics dashboard

# Contact
* Vikas G J
* Email: vikasgjv@gmail.com
* LinkedIn: linkedin.com/in/vikas-gj-979251296
* 
## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- FastAPI for the excellent web framework
- Chart.js for beautiful visualizations

---

⭐ Star this repo if you find it useful!
