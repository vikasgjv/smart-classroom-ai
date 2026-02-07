# 🌟 ClassAI Features Documentation

Complete guide to all features and capabilities.

## 📊 Core Monitoring Features

### 1. Real-Time Attention Tracking
- **Continuous Monitoring**: Updates every 3 seconds
- **Attention Score**: 0-100% based on face and eye detection
- **Visual Feedback**: Large circular display with color coding
- **Status Indicators**: Emoji-based engagement levels

**How it works:**
- Detects face presence using Haar Cascade
- Analyzes eye detection for attention level
- Calculates attention score based on multiple factors
- Updates database in real-time

### 2. Color-Coded Engagement System

| Color | Range | Meaning | Emoji |
|-------|-------|---------|-------|
| 🟢 Green | 80-100% | High Focus | 😊 |
| 🟠 Orange | 50-79% | Medium Focus | 😐 |
| 🔴 Red | 0-49% | Low Focus | 😴 |
| ⚪ Gray | N/A | No Face Detected | 👤 |

### 3. Face Detection
- **Multi-Level Sensitivity**: 4-level cascade detection
- **Glasses Support**: Enhanced eye detection for spectacles
- **Profile Detection**: Works with slight head turns
- **Quality Assessment**: Validates face detection accuracy

**Detection Parameters:**
```python
- Minimum face size: 60x60 pixels
- Scale factor: 1.1
- Minimum neighbors: 3-6 (adaptive)
- Eye detection: Both eyes required for high attention
```

### 4. Absence Tracking
- **Automatic Detection**: Identifies when student is not present
- **Time Tracking**: Records exact minutes absent
- **Attendance Rate**: Calculates percentage present
- **Visual Indicator**: Shows "No face detected" message

## 🌙 Dark Mode

### Features
- **Toggle Button**: Fixed position in top-right corner
- **Persistent Storage**: Saves preference in localStorage
- **Smooth Transitions**: All colors transition smoothly (0.3s)
- **Chart Adaptation**: Chart colors automatically adjust
- **System-Wide**: Affects all UI elements

### Color Schemes

**Light Mode:**
- Background: #f5f7fa
- Cards: #ffffff
- Text: #2c3e50
- Accent: #3498db

**Dark Mode:**
- Background: #1a1a2e
- Cards: #0f3460
- Text: #eaeaea
- Accent: #3498db

### Usage
```javascript
// Toggle programmatically
document.documentElement.setAttribute('data-theme', 'dark');

// Check current theme
const theme = document.documentElement.getAttribute('data-theme');
```

## ⚠️ Absence Alert System

### Configuration
- **Default Threshold**: 2 minutes
- **Check Interval**: Every 1 second
- **Alert Duration**: 10 seconds (auto-dismiss)
- **Manual Close**: Click X button

### How It Works
1. System checks for face detection every second
2. If no face detected, starts timer
3. After 2 minutes, triggers alert banner
4. Alert appears at top of screen
5. Auto-dismisses after 10 seconds
6. Can be manually closed

### Customization
Change threshold in `script.js`:
```javascript
const ABSENCE_ALERT_THRESHOLD = 2; // Minutes
```

### Alert Behavior
- **Red Banner**: Appears at top of screen
- **Warning Icon**: ⚠️ emoji
- **Message**: "Student has been absent for X minutes!"
- **Non-Blocking**: Doesn't interrupt monitoring
- **Repeating**: Re-alerts every 2 minutes if still absent

## 📄 PDF Export

### Features
- **One-Click Export**: Single button press
- **Professional Format**: Clean, formatted layout
- **Auto-Naming**: `ClassAI_Report_YYYY-MM-DD.pdf`
- **Complete Data**: All report sections included
- **High Quality**: 98% JPEG quality, 2x scale

### Export Options
```javascript
const pdfOptions = {
    margin: 10,
    filename: 'ClassAI_Report_2026-02-07.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
};
```

### What's Included
- Session summary (date, duration, student ID)
- Attention metrics (average, peak, lowest)
- Attendance rate and time missed
- Performance indicators and grade
- Strengths and recommendations

### Requirements
- Internet connection (for html2pdf.js CDN)
- Modern browser with download capability
- Report must be generated first

## 📈 Live Charts

### Attention Timeline
- **Type**: Line chart with area fill
- **Update Frequency**: Every 3 seconds
- **Data Points**: Last 20 readings (1 minute)
- **Smooth Curves**: Tension: 0.4
- **Interactive**: Hover for exact values

### Chart Features
- **Auto-Scaling**: Y-axis 0-100%
- **Time Labels**: HH:MM format
- **Color Coding**: Blue gradient
- **Responsive**: Adapts to screen size
- **Theme Support**: Colors change with dark mode

### Customization
```javascript
// Change data retention
if (chartData.labels.length > 20) {  // Change 20 to desired value
    chartData.labels.shift();
    chartData.datasets[0].data.shift();
}
```

## 📊 Session Statistics

### Real-Time Metrics

**1. Average Attention**
- Calculated from all valid readings
- Excludes "no face" periods
- Updates every 3 seconds
- Displayed as percentage

**2. Peak Attention**
- Highest attention score in session
- Tracks best performance moment
- Useful for identifying optimal focus times

**3. Lowest Attention**
- Minimum attention score recorded
- Helps identify problem periods
- Excludes absence periods

**4. Absence Time**
- Total minutes with no face detected
- Cumulative throughout session
- Updates in real-time
- Displayed in minutes

### Statistics Display
- **Icon-Based**: Visual indicators for each metric
- **Large Numbers**: Easy to read at a glance
- **Hover Effects**: Interactive feedback
- **Color-Coded**: Primary blue for values

## 📋 Report Generation

### Report Sections

**1. Session Summary**
- Student ID
- Session date and time
- Total duration (minutes)
- Overall performance score (0-100)

**2. Attention Summary**
- Average attention percentage
- Attention grade (A-F)
- Peak attention score
- Attendance rate
- Time missed (minutes)

**3. Performance Indicators**
- Overall score
- Strengths list
- Areas for improvement
- Engagement level

**4. Recommendations**
- Personalized suggestions
- Based on attention patterns
- Actionable advice
- Improvement strategies

### Grading System
```
A: 90-100% - Excellent
B: 80-89%  - Very Good
C: 70-79%  - Good
D: 60-69%  - Satisfactory
F: 0-59%   - Needs Improvement
```

### Report Storage
- **Format**: JSON and HTML
- **Location**: Project root directory
- **Naming**: `report_[StudentID]_[Timestamp].[ext]`
- **Database**: Also stored in SQLite

## 🎨 User Interface

### Modern Design Elements

**1. Card-Based Layout**
- Rounded corners (16px)
- Subtle shadows
- Hover effects (lift on hover)
- Smooth transitions

**2. Animations**
- Pulse effect on attention circle
- Fade transitions for updates
- Slide-down for alerts
- Scale on button hover

**3. Responsive Design**
- Desktop: Multi-column grid
- Tablet: 2-column layout
- Mobile: Single column
- Breakpoint: 768px

**4. Typography**
- Font: Segoe UI, system fonts
- Hierarchy: Clear size differences
- Weights: 400 (normal), 600 (semibold), 700 (bold)
- Line height: 1.6 for readability

### Color System
- **Primary**: #3498db (Blue)
- **Success**: #27ae60 (Green)
- **Warning**: #f39c12 (Orange)
- **Danger**: #e74c3c (Red)
- **Info**: #16a085 (Teal)

### Accessibility
- High contrast ratios
- Large touch targets (44px minimum)
- Keyboard navigation support
- Screen reader friendly
- Focus indicators

## 🔄 Real-Time Updates

### Update Cycle
1. **Every 3 seconds:**
   - Fetch attention data from API
   - Update attention display
   - Update engagement status
   - Add point to chart
   - Update statistics
   - Update time running
   - Update last update timestamp

2. **Every 1 second:**
   - Check for absence
   - Update absence timer
   - Trigger alerts if needed

### Data Flow
```
Webcam → OpenCV Detection → Database → API → Frontend → Display
```

### Performance
- **Webcam FPS**: 30 (processes every 2nd frame)
- **API Response**: <100ms typical
- **UI Update**: <50ms
- **Memory Usage**: ~200MB typical
- **CPU Usage**: 10-20% on modern hardware

## 🎯 Best Practices

### For Teachers
1. **Good Lighting**: Ensure adequate lighting for face detection
2. **Camera Position**: Place camera at eye level
3. **Stable Setup**: Avoid moving camera during session
4. **Regular Checks**: Monitor the dashboard periodically
5. **End Sessions**: Always click "End Class" properly

### For Students
1. **Face Camera**: Look at camera regularly
2. **Stay Centered**: Keep face in frame
3. **Good Posture**: Sit upright for better detection
4. **Minimize Movement**: Avoid excessive head movement
5. **Lighting**: Ensure face is well-lit

### For Administrators
1. **Test First**: Run test sessions before deployment
2. **Network Setup**: Ensure stable network connection
3. **Backup Data**: Regular database backups
4. **Monitor Performance**: Check system resources
5. **Update Regularly**: Keep dependencies updated

## 🔮 Advanced Features (Coming Soon)

- Multi-student monitoring
- Emotion detection
- Hand raise detection
- Screen sharing detection
- Integration with LMS
- Mobile app
- Advanced analytics dashboard
- AI-powered insights

---

**For more information, see [README.md](README.md) and [SETUP.md](SETUP.md)**
