# 🚀 ClassAI Setup Guide

Complete step-by-step installation and setup instructions.

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Webcam**: Built-in or USB webcam (720p or higher)
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, or Edge 90+

### Recommended Requirements
- **RAM**: 8GB or more
- **Webcam**: 1080p HD webcam
- **Internet**: For downloading dependencies and CDN resources

## 🔧 Installation Steps

### Step 1: Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer and **check "Add Python to PATH"**
3. Verify installation:
```bash
python --version
```

#### macOS
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/ClassAI.git
cd ClassAI
```

Or download ZIP and extract.

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI - Web framework
- Uvicorn - ASGI server
- OpenCV - Computer vision
- SQLAlchemy - Database ORM
- NumPy - Numerical computing

### Step 5: Verify Installation

```bash
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import fastapi; print('FastAPI installed')"
```

## 🎬 Running the Application

### Method 1: Two Terminal Windows

**Terminal 1 - Backend Server:**
```bash
cd ClassAI
python main.py
```
You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
```

**Terminal 2 - Frontend Server:**
```bash
cd ClassAI
python -m http.server 3001
```
You should see:
```
Serving HTTP on 0.0.0.0 port 3001
```

### Method 2: Using Start Scripts

Create `start.sh` (macOS/Linux) or `start.bat` (Windows):

**start.sh:**
```bash
#!/bin/bash
python main.py &
python -m http.server 3001
```

**start.bat:**
```batch
@echo off
start python main.py
start python -m http.server 3001
```

### Step 6: Access Dashboard

Open your browser and go to:
```
http://localhost:3001
```

## 🔍 Troubleshooting

### Issue: "Module not found" error
**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Webcam not detected
**Solution:**
- Check webcam permissions in system settings
- Try different camera index in `continuous_webcam.py`:
```python
cap = cv2.VideoCapture(0)  # Try 0, 1, 2, etc.
```

### Issue: Port already in use
**Solution:**
```bash
# Find and kill process using port 8001
# macOS/Linux:
lsof -ti:8001 | xargs kill -9

# Windows:
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

### Issue: Face detection not working
**Solution:**
- Ensure good lighting
- Face the camera directly
- Check if `models_ai/haarcascade_frontalface_default.xml` exists
- Try adjusting detection sensitivity in `continuous_webcam.py`

### Issue: Dark mode not working
**Solution:**
- Clear browser cache (Ctrl+Shift+Delete)
- Hard reload (Ctrl+F5 or Cmd+Shift+R)
- Check browser console for JavaScript errors (F12)

### Issue: PDF export fails
**Solution:**
- Check internet connection (needs CDN for html2pdf.js)
- Ensure popup blocker is disabled
- Try different browser

## 🌐 Network Setup (Multiple Students)

### Find Your IP Address

**Windows:**
```bash
ipconfig
# Look for "IPv4 Address"
```

**macOS/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
# Or
ip addr show
```

### Configure Firewall

**Windows:**
1. Windows Defender Firewall → Advanced Settings
2. Inbound Rules → New Rule
3. Port → TCP → 3001, 8001
4. Allow the connection

**macOS:**
```bash
# System Preferences → Security & Privacy → Firewall → Firewall Options
# Add Python to allowed apps
```

**Linux (UFW):**
```bash
sudo ufw allow 3001
sudo ufw allow 8001
```

### Students Connect

Students on the same network can access:
```
http://YOUR-IP-ADDRESS:3001
```

Example: `http://192.168.1.100:3001`

## 🐳 Docker Setup (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001 3001

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t classai .
docker run -p 8001:8001 -p 3001:3001 classai
```

## 📱 Testing

### Test Backend API
```bash
curl http://localhost:8001/docs
```

### Test Frontend
```bash
curl http://localhost:3001
```

### Run System Test
```bash
python -c "
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print('Webcam test:', 'PASS' if ret else 'FAIL')
cap.release()
"
```

## 🔐 Security Considerations

### For Production Deployment:
1. Use HTTPS (SSL/TLS certificates)
2. Add authentication (JWT tokens)
3. Implement rate limiting
4. Use environment variables for secrets
5. Enable CORS properly
6. Use reverse proxy (nginx)

### Example nginx config:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3001;
    }

    location /api {
        proxy_pass http://localhost:8001;
    }
}
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenCV Tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 💡 Tips

1. **Use virtual environment** to avoid dependency conflicts
2. **Keep Python updated** for security and performance
3. **Test webcam** before starting a session
4. **Good lighting** improves face detection accuracy
5. **Close other apps** using webcam before starting
6. **Regular backups** of the database file

## 🆘 Getting Help

If you encounter issues:
1. Check this guide first
2. Search existing GitHub issues
3. Open a new issue with:
   - Error message
   - Python version
   - Operating system
   - Steps to reproduce

---

**Ready to start? Run `python main.py` and open `http://localhost:3001`!** 🚀
