# ⚡ ClassAI Quick Start Guide

Get ClassAI running in 5 minutes!

## 🎯 Prerequisites
- Python 3.8+ installed
- Webcam connected
- Modern web browser

## 🚀 Installation (3 Steps)

### Step 1: Download
```bash
git clone https://github.com/yourusername/ClassAI.git
cd ClassAI
```

### Step 2: Install
```bash
pip install -r requirements.txt
```

### Step 3: Run
```bash
# macOS/Linux
./start.sh

# Windows
start.bat

# Or manually:
python main.py
# Then in another terminal:
python -m http.server 3001
```

## 🎓 Using ClassAI

### 1. Open Dashboard
```
http://localhost:3001
```

### 2. Start Monitoring
- Click **"Start Class"**
- Allow webcam access
- System starts monitoring automatically

### 3. Monitor Student
- Watch real-time attention score
- Check engagement status
- View live chart updates

### 4. Generate Report
- Click **"End Class"**
- Click **"Generate Report"**
- Click **"Export PDF"** to save

## 🌙 Quick Features

### Dark Mode
Click moon/sun icon (top-right corner)

### Absence Alerts
Automatic alert after 2 minutes of absence

### PDF Export
One-click report export to PDF

## 🎨 Understanding Colors

| Color | Meaning |
|-------|---------|
| 🟢 Green | High attention (80%+) |
| 🟠 Orange | Medium attention (50-79%) |
| 🔴 Red | Low attention (<50%) |
| ⚪ Gray | Student absent |

## 🔧 Troubleshooting

### Webcam not working?
```python
# Try different camera index in continuous_webcam.py
cap = cv2.VideoCapture(1)  # Try 0, 1, 2
```

### Port already in use?
```bash
# Kill process on port 8001
lsof -ti:8001 | xargs kill -9  # macOS/Linux
```

### Module not found?
```bash
pip install --upgrade -r requirements.txt
```

## 📱 Network Access

### Find Your IP
```bash
# macOS/Linux
ifconfig | grep "inet "

# Windows
ipconfig
```

### Students Connect
```
http://YOUR-IP:3001
```

## 📚 Next Steps

- Read [FEATURES.md](FEATURES.md) for detailed features
- Check [SETUP.md](SETUP.md) for advanced setup
- See [README.md](README.md) for complete documentation

## 🆘 Need Help?

- Check [SETUP.md](SETUP.md) troubleshooting section
- Open an issue on GitHub
- Read the documentation

---

**That's it! You're ready to use ClassAI! 🎉**
