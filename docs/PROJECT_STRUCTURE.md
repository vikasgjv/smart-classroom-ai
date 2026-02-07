# 📁 ClassAI Project Structure

Complete overview of the project organization and file purposes.

## 🌳 Directory Tree

```
ClassAI/
├── .github/
│   └── workflows/
│       └── test.yml              # GitHub Actions CI/CD
├── models_ai/
│   └── haarcascade_frontalface_default.xml  # Face detection model
├── .gitignore                    # Git ignore rules
├── CONTRIBUTING.md               # Contribution guidelines
├── FEATURES.md                   # Detailed features documentation
├── LICENSE                       # MIT License
├── PROJECT_STRUCTURE.md          # This file
├── QUICKSTART.md                 # Quick start guide
├── README.md                     # Main documentation
├── SETUP.md                      # Installation and setup guide
├── continuous_webcam.py          # Webcam monitoring & face detection
├── database.py                   # Database operations
├── index.html                    # Frontend dashboard
├── main.py                       # FastAPI backend server
├── models.py                     # SQLAlchemy data models
├── report_generator.py           # Report generation logic
├── requirements.txt              # Python dependencies
├── script.js                     # Frontend JavaScript
├── start.bat                     # Windows start script
├── start.sh                      # macOS/Linux start script
└── style.css                     # Frontend styling with dark mode
```

## 📄 File Descriptions

### Core Application Files

#### `main.py`
**Purpose**: FastAPI backend server and API endpoints

**Key Components**:
- FastAPI application initialization
- CORS middleware configuration
- API endpoints:
  - `/start-monitoring` - Start webcam monitoring
  - `/stop-monitoring` - Stop webcam monitoring
  - `/live-attention` - Get real-time attention data
  - `/generate-report` - Generate session report
  - `/get-attention-data` - Retrieve historical data

**Dependencies**: FastAPI, Uvicorn, SQLAlchemy

**Port**: 8001

---

#### `continuous_webcam.py`
**Purpose**: Webcam monitoring and face detection engine

**Key Components**:
- OpenCV webcam capture
- Face detection using Haar Cascades
- Eye detection for attention scoring
- Multi-level sensitivity detection
- Background thread processing
- Database integration for storing readings

**Key Functions**:
- `start_monitoring()` - Initialize webcam and start monitoring
- `stop_monitoring()` - Stop monitoring and cleanup
- `detect_face_and_attention()` - Core detection logic
- `calculate_attention_score()` - Compute attention percentage

**Detection Features**:
- 4-level cascade sensitivity
- Glasses/spectacles support
- Profile face detection
- Quality assessment
- Temporal smoothing

---

#### `database.py`
**Purpose**: Database operations and management

**Key Components**:
- SQLite database initialization
- Session management
- CRUD operations for attention readings
- Database schema creation

**Key Functions**:
- `init_db()` - Initialize database
- `get_db()` - Get database session
- `save_attention_reading()` - Store attention data
- `get_attention_history()` - Retrieve historical data

**Database**: SQLite (`smart_classroom.db`)

---

#### `models.py`
**Purpose**: SQLAlchemy data models

**Models**:
- `AttentionReading` - Stores attention measurements
  - `id` - Primary key
  - `student_id` - Student identifier
  - `timestamp` - Reading time
  - `attention_score` - Attention percentage (0-1)
  - `face_detected` - Boolean
  - `eyes_detected` - Number of eyes (0-2)
  - `detection_status` - Status string

---

#### `report_generator.py`
**Purpose**: Generate comprehensive session reports

**Key Components**:
- Data aggregation and analysis
- Performance metrics calculation
- Grading system (A-F)
- Recommendations generation
- HTML and JSON report creation

**Key Functions**:
- `generate_student_report()` - Main report generation
- `calculate_metrics()` - Compute statistics
- `generate_insights()` - Create recommendations
- `create_html_report()` - Format HTML output

**Report Sections**:
- Session summary
- Attention metrics
- Performance indicators
- Strengths and weaknesses
- Personalized recommendations

---

### Frontend Files

#### `index.html`
**Purpose**: Main dashboard interface

**Sections**:
- Header with branding
- Dark mode toggle button
- Absence alert banner
- Session control panel
- Live attention monitor
- Attention timeline chart
- Statistics dashboard
- Report display section

**External Libraries**:
- Chart.js (for charts)
- html2pdf.js (for PDF export)

---

#### `script.js`
**Purpose**: Frontend logic and interactivity

**Key Features**:
- Dark mode management
- Real-time data fetching
- Chart updates
- Absence monitoring
- Alert system
- PDF export
- Report generation
- WebSocket-ready architecture

**Key Functions**:
- `toggleTheme()` - Dark mode toggle
- `toggleClass()` - Start/stop session
- `updateAttentionMetrics()` - Fetch and display data
- `checkAbsence()` - Monitor absence
- `generateStudentReport()` - Create report
- `exportReportToPDF()` - Export to PDF

**Update Intervals**:
- Attention data: 3 seconds
- Absence check: 1 second
- Chart update: 3 seconds

---

#### `style.css`
**Purpose**: Styling and visual design

**Key Features**:
- CSS variables for theming
- Dark mode support
- Responsive design
- Animations and transitions
- Card-based layout
- Color-coded attention system

**Themes**:
- Light mode (default)
- Dark mode (toggle)

**Breakpoints**:
- Desktop: >768px
- Mobile: ≤768px

---

### AI Models

#### `models_ai/haarcascade_frontalface_default.xml`
**Purpose**: Pre-trained face detection model

**Details**:
- OpenCV Haar Cascade classifier
- Trained on thousands of face images
- Detects frontal faces
- Fast and efficient
- No GPU required

---

### Documentation Files

#### `README.md`
Main project documentation with overview, features, installation, and usage.

#### `QUICKSTART.md`
5-minute quick start guide for new users.

#### `SETUP.md`
Detailed installation and configuration instructions.

#### `FEATURES.md`
Comprehensive feature documentation with examples.

#### `CONTRIBUTING.md`
Guidelines for contributing to the project.

#### `PROJECT_STRUCTURE.md`
This file - project organization overview.

---

### Configuration Files

#### `requirements.txt`
Python package dependencies:
```
fastapi>=0.68.0
uvicorn>=0.15.0
opencv-python>=4.5.0
sqlalchemy>=1.4.0
numpy>=1.21.0
python-multipart>=0.0.5
```

#### `.gitignore`
Files and directories to exclude from Git:
- Python cache files
- Virtual environments
- Database files
- Generated reports
- Debug files
- IDE configurations

#### `LICENSE`
MIT License - open source and permissive.

---

### Scripts

#### `start.sh` (macOS/Linux)
Bash script to start both servers:
1. Check Python installation
2. Install dependencies if needed
3. Start backend server (background)
4. Start frontend server (foreground)

#### `start.bat` (Windows)
Batch script for Windows:
1. Check Python installation
2. Install dependencies if needed
3. Start backend in new window
4. Start frontend in current window

---

### CI/CD

#### `.github/workflows/test.yml`
GitHub Actions workflow:
- Runs on push and pull requests
- Tests on multiple OS (Ubuntu, Windows, macOS)
- Tests Python 3.8, 3.9, 3.10, 3.11
- Checks syntax and imports

---

## 🔄 Data Flow

```
User Browser (index.html)
    ↓
JavaScript (script.js)
    ↓
FastAPI Server (main.py)
    ↓
Webcam Monitor (continuous_webcam.py)
    ↓
OpenCV Face Detection
    ↓
Database (database.py)
    ↓
Report Generator (report_generator.py)
    ↓
PDF Export (html2pdf.js)
```

## 🗄️ Database Schema

```sql
CREATE TABLE attention_readings (
    id INTEGER PRIMARY KEY,
    student_id VARCHAR(50),
    timestamp DATETIME,
    attention_score FLOAT,
    face_detected BOOLEAN,
    eyes_detected INTEGER,
    detection_status VARCHAR(50)
);
```

## 🌐 API Architecture

```
Frontend (Port 3001)
    ↓ HTTP Requests
Backend API (Port 8001)
    ↓ Database Queries
SQLite Database
    ↓ Webcam Data
OpenCV Processing
```

## 📦 Dependencies

### Python Packages
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **OpenCV**: Computer vision
- **SQLAlchemy**: Database ORM
- **NumPy**: Numerical computing

### JavaScript Libraries (CDN)
- **Chart.js**: Data visualization
- **html2pdf.js**: PDF generation

## 🔐 Security Considerations

### Current Implementation
- Local-only deployment
- No authentication required
- CORS enabled for localhost
- Data stored locally

### Production Recommendations
- Add JWT authentication
- Implement HTTPS
- Use environment variables
- Add rate limiting
- Implement RBAC
- Use reverse proxy

## 🚀 Deployment Options

### Local Development
```bash
python main.py
python -m http.server 3001
```

### Local Network
```bash
# Find IP and share with students
ifconfig | grep "inet "
```

### Cloud Deployment
- AWS EC2
- Google Cloud Compute
- DigitalOcean Droplet
- Heroku
- Docker container

## 📊 Performance Metrics

### Resource Usage
- **CPU**: 10-20% (single student)
- **RAM**: ~200MB
- **Disk**: ~50MB (excluding database)
- **Network**: Minimal (local only)

### Processing Speed
- **Webcam FPS**: 30 (processes every 2nd frame)
- **API Response**: <100ms
- **Face Detection**: ~30ms per frame
- **Database Write**: <10ms

## 🔮 Future Structure

Planned additions:
```
ClassAI/
├── tests/                    # Unit and integration tests
├── config/                   # Configuration files
├── logs/                     # Application logs
├── static/                   # Static assets
├── templates/                # Email templates
├── utils/                    # Utility functions
└── api/                      # API versioning
    ├── v1/
    └── v2/
```

---

**For more information, see other documentation files in the project root.**
