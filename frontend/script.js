// ClassAI Enhanced Script with Dark Mode, PDF Export, and Absence Alerts

// Global state
let isClassActive = false;
let startTime = null;
let sessionStartTime = null;
let attentionChart = null;
let updateInterval = null;
let absenceCheckInterval = null;
let absenceStartTime = null;
let totalAbsenceTime = 0;

// Alert settings
const ABSENCE_ALERT_THRESHOLD = 2; // Alert after 2 minutes of absence

// Chart data
const chartData = {
    labels: [],
    datasets: [{
        label: 'Attention %',
        data: [],
        borderColor: '#3498db',
        backgroundColor: 'rgba(52, 152, 219, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6
    }]
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeChart();
    setupEventListeners();
    updateLastUpdateTime();
    generateInitialData();
});

// Theme Management
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    
    // Update chart colors
    if (attentionChart) {
        updateChartTheme(newTheme);
    }
}

function updateThemeIcon(theme) {
    const icon = document.querySelector('.theme-icon');
    icon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

function updateChartTheme(theme) {
    const textColor = theme === 'dark' ? '#eaeaea' : '#2c3e50';
    const gridColor = theme === 'dark' ? '#2a2a3e' : '#e1e8ed';
    
    attentionChart.options.scales.y.ticks.color = textColor;
    attentionChart.options.scales.x.ticks.color = textColor;
    attentionChart.options.scales.y.grid.color = gridColor;
    attentionChart.options.scales.x.grid.color = gridColor;
    attentionChart.update();
}

// Event Listeners
function setupEventListeners() {
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    document.getElementById('classToggle').addEventListener('click', toggleClass);
    document.getElementById('generateReport').addEventListener('click', generateStudentReport);
    document.getElementById('exportPDF').addEventListener('click', exportReportToPDF);
}

// Initialize Chart
function initializeChart() {
    const ctx = document.getElementById('attentionChart').getContext('2d');
    const theme = document.documentElement.getAttribute('data-theme');
    const textColor = theme === 'dark' ? '#eaeaea' : '#2c3e50';
    const gridColor = theme === 'dark' ? '#2a2a3e' : '#e1e8ed';
    
    attentionChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        },
                        color: textColor
                    },
                    grid: {
                        color: gridColor
                    }
                },
                x: {
                    ticks: {
                        color: textColor
                    },
                    grid: {
                        color: gridColor
                    }
                }
            },
            elements: {
                point: {
                    radius: 4,
                    hoverRadius: 6
                }
            }
        }
    });
}

// Toggle Class Session
async function toggleClass() {
    const button = document.getElementById('classToggle');
    const sessionStatus = document.getElementById('sessionStatus');
    const reportButton = document.getElementById('generateReport');
    const exportButton = document.getElementById('exportPDF');
    
    if (!isClassActive) {
        // Start class
        isClassActive = true;
        startTime = new Date();
        sessionStartTime = new Date();
        absenceStartTime = null;
        totalAbsenceTime = 0;
        
        button.innerHTML = '<span class="btn-icon">⏸️</span> End Class';
        button.classList.add('active');
        sessionStatus.textContent = 'Active';
        sessionStatus.style.color = '#27ae60';
        reportButton.disabled = true;
        exportButton.disabled = true;
        
        // Start continuous monitoring
        await startContinuousMonitoring();
        
        // Start live updates
        startLiveUpdates();
        
        // Start absence monitoring
        startAbsenceMonitoring();
        
        showNotification('Class session started successfully!', 'success');
    } else {
        // End class
        isClassActive = false;
        startTime = null;
        
        button.innerHTML = '<span class="btn-icon">▶️</span> Start Class';
        button.classList.remove('active');
        sessionStatus.textContent = 'Inactive';
        sessionStatus.style.color = '#95a5a6';
        reportButton.disabled = false;
        exportButton.disabled = false;
        
        // Stop continuous monitoring
        await stopContinuousMonitoring();
        
        // Stop live updates
        stopLiveUpdates();
        
        // Stop absence monitoring
        stopAbsenceMonitoring();
        
        showNotification('Class session ended. You can now generate a report.', 'info');
    }
}

// Start/Stop Continuous Monitoring
async function startContinuousMonitoring() {
    try {
        const response = await fetch("http://127.0.0.1:8001/start-monitoring", {
            method: "POST"
        });
        const data = await response.json();
        console.log('Monitoring started:', data);
    } catch (error) {
        console.error('Error starting monitoring:', error);
    }
}

async function stopContinuousMonitoring() {
    try {
        const response = await fetch("http://127.0.0.1:8001/stop-monitoring", {
            method: "POST"
        });
        const data = await response.json();
        console.log('Monitoring stopped:', data);
    } catch (error) {
        console.error('Error stopping monitoring:', error);
    }
}

// Live Updates
function startLiveUpdates() {
    updateInterval = setInterval(() => {
        updateAttentionMetrics();
        updateTimeRunning();
        updateChart();
        updateLastUpdateTime();
        updateStatistics();
    }, 3000);
}

function stopLiveUpdates() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
}

// Absence Monitoring
function startAbsenceMonitoring() {
    absenceCheckInterval = setInterval(checkAbsence, 1000); // Check every second
}

function stopAbsenceMonitoring() {
    if (absenceCheckInterval) {
        clearInterval(absenceCheckInterval);
        absenceCheckInterval = null;
    }
    absenceStartTime = null;
}

function checkAbsence() {
    const attentionElement = document.getElementById('attentionValue');
    const isAbsent = attentionElement.textContent === "No face detected";
    
    if (isAbsent) {
        if (!absenceStartTime) {
            absenceStartTime = new Date();
        } else {
            const absenceDuration = (new Date() - absenceStartTime) / 1000 / 60; // minutes
            
            if (absenceDuration >= ABSENCE_ALERT_THRESHOLD) {
                showAbsenceAlert(Math.floor(absenceDuration));
                // Reset to avoid repeated alerts
                absenceStartTime = new Date(new Date() - (ABSENCE_ALERT_THRESHOLD - 0.5) * 60 * 1000);
            }
        }
        totalAbsenceTime = (new Date() - absenceStartTime) / 1000 / 60;
    } else {
        if (absenceStartTime) {
            totalAbsenceTime += (new Date() - absenceStartTime) / 1000 / 60;
        }
        absenceStartTime = null;
    }
    
    // Update absence time display
    document.getElementById('absenceTime').textContent = Math.floor(totalAbsenceTime) + ' min';
}

function showAbsenceAlert(minutes) {
    const message = `⚠️ Student has been absent for ${minutes} minutes!`;
    showAlert(message);
}

function showAlert(message) {
    const banner = document.getElementById('alertBanner');
    const messageElement = document.getElementById('alertMessage');
    
    messageElement.textContent = message;
    banner.style.display = 'flex';
    
    // Auto-hide after 10 seconds
    setTimeout(() => {
        closeAlert();
    }, 10000);
}

function closeAlert() {
    document.getElementById('alertBanner').style.display = 'none';
}

// Update Attention Metrics
async function updateAttentionMetrics() {
    if (!isClassActive) return;

    try {
        const response = await fetch("http://127.0.0.1:8001/live-attention", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                student_id: "S01"
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const attention = Math.round(data.live_attention_score * 100);
        const detectionStatus = data.detection_status;

        const attentionElement = document.getElementById('attentionValue');
        
        // Add animation
        attentionElement.classList.add('updating');
        setTimeout(() => {
            attentionElement.classList.remove('updating');
        }, 500);
        
        // Show different display based on detection status
        if (detectionStatus === "no_face_detected") {
            attentionElement.textContent = "No face detected";
            attentionElement.classList.remove('high-attention', 'medium-attention', 'low-attention');
            attentionElement.classList.add('no-face');
            
            updateEngagementStatus(0, true);
        } else {
            attentionElement.textContent = attention + '%';
            attentionElement.classList.remove('no-face');
            updateAttentionColor(attention);
            updateEngagementStatus(attention, false);
        }
        
    } catch (error) {
        console.error('Error fetching attention data:', error);
    }
}

function updateAttentionColor(attention) {
    const attentionElement = document.getElementById('attentionValue');
    attentionElement.classList.remove('high-attention', 'medium-attention', 'low-attention');
    
    if (attention >= 80) {
        attentionElement.classList.add('high-attention');
    } else if (attention >= 50) {
        attentionElement.classList.add('medium-attention');
    } else {
        attentionElement.classList.add('low-attention');
    }
}

function updateEngagementStatus(attention, noFaceDetected = false) {
    const statusElement = document.getElementById('statusLevel');
    const emojiElement = document.getElementById('statusEmoji');
    
    if (noFaceDetected) {
        statusElement.textContent = 'No Student';
        statusElement.style.color = '#95a5a6';
        emojiElement.textContent = '👤';
    } else if (attention >= 80) {
        statusElement.textContent = 'High Focus';
        statusElement.style.color = '#27ae60';
        emojiElement.textContent = '😊';
    } else if (attention >= 50) {
        statusElement.textContent = 'Medium Focus';
        statusElement.style.color = '#f39c12';
        emojiElement.textContent = '😐';
    } else {
        statusElement.textContent = 'Low Focus';
        statusElement.style.color = '#e74c3c';
        emojiElement.textContent = '😴';
    }
}

// Update Time Running
function updateTimeRunning() {
    if (!isClassActive || !startTime) return;
    
    const now = new Date();
    const diff = Math.floor((now - startTime) / 1000 / 60);
    document.getElementById('timeRunning').textContent = `${diff} mins`;
}

// Update Chart
function updateChart() {
    if (!isClassActive) return;
    
    const now = new Date();
    const timeLabel = now.toLocaleTimeString('en-US', { 
        hour12: false, 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    const attentionElement = document.getElementById('attentionValue');
    let attention = 0;
    
    if (attentionElement.textContent === "No face detected") {
        attention = 0;
    } else {
        attention = parseInt(attentionElement.textContent);
    }
    
    chartData.labels.push(timeLabel);
    chartData.datasets[0].data.push(attention);
    
    // Keep only last 20 data points
    if (chartData.labels.length > 20) {
        chartData.labels.shift();
        chartData.datasets[0].data.shift();
    }
    
    attentionChart.update('none');
}

// Update Statistics
function updateStatistics() {
    if (chartData.datasets[0].data.length === 0) return;
    
    const data = chartData.datasets[0].data;
    const validData = data.filter(v => v > 0);
    
    if (validData.length > 0) {
        const avg = Math.round(validData.reduce((a, b) => a + b, 0) / validData.length);
        const peak = Math.max(...validData);
        const lowest = Math.min(...validData);
        
        document.getElementById('avgAttention').textContent = avg + '%';
        document.getElementById('peakAttention').textContent = peak + '%';
        document.getElementById('lowestAttention').textContent = lowest + '%';
    }
}

// Generate Initial Data
function generateInitialData() {
    const now = new Date();
    
    for (let i = 9; i >= 0; i--) {
        const time = new Date(now.getTime() - (i * 3 * 60 * 1000));
        const timeLabel = time.toLocaleTimeString('en-US', { 
            hour12: false, 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        const attention = Math.floor(Math.random() * 25) + 70;
        
        chartData.labels.push(timeLabel);
        chartData.datasets[0].data.push(attention);
    }
    
    if (attentionChart) {
        attentionChart.update();
    }
}

// Generate Report
async function generateStudentReport() {
    const reportButton = document.getElementById('generateReport');
    const originalText = reportButton.innerHTML;
    
    try {
        reportButton.innerHTML = '<span class="btn-icon">⏳</span> Generating...';
        reportButton.disabled = true;
        
        const sessionEnd = new Date();
        const requestData = {
            student_id: "S01",
            session_start: sessionStartTime ? sessionStartTime.toISOString() : new Date(Date.now() - 3600000).toISOString(),
            session_end: sessionEnd.toISOString()
        };
        
        const response = await fetch("http://127.0.0.1:8001/generate-report", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.status === "success") {
            displayReport(data.report);
            document.getElementById('exportPDF').disabled = false;
            showNotification('Report generated successfully!', 'success');
        } else {
            throw new Error(data.message || 'Failed to generate report');
        }
        
    } catch (error) {
        console.error('Error generating report:', error);
        showNotification('Error generating report: ' + error.message, 'error');
    } finally {
        reportButton.innerHTML = originalText;
        reportButton.disabled = false;
    }
}

// Display Report
function displayReport(report) {
    const reportSection = document.getElementById('reportSection');
    const reportContent = document.getElementById('reportContent');
    
    const html = `
        <div class="report-summary">
            <h3>📊 Session Summary</h3>
            <div class="report-grid">
                <div class="report-item">
                    <strong>Student ID:</strong> ${report.student_info.student_id}
                </div>
                <div class="report-item">
                    <strong>Date:</strong> ${report.student_info.session_date}
                </div>
                <div class="report-item">
                    <strong>Duration:</strong> ${report.student_info.duration_minutes} minutes
                </div>
                <div class="report-item">
                    <strong>Overall Score:</strong> ${report.performance_indicators.overall_score}/100
                </div>
            </div>
        </div>
        
        <div class="report-section-content">
            <h3>📈 Attention Summary</h3>
            <p><strong>Average Attention:</strong> ${report.attention_summary.average_attention}%</p>
            <p><strong>Grade:</strong> ${report.attention_summary.attention_grade}</p>
            <p><strong>Peak Attention:</strong> ${report.attention_summary.peak_attention}%</p>
            <p><strong>Attendance Rate:</strong> ${report.attention_summary.attendance_rate}%</p>
            <p><strong>Time Missed:</strong> ${report.attention_summary.time_missed_minutes} minutes</p>
        </div>
        
        <div class="report-section-content">
            <h3>💪 Strengths</h3>
            <ul>
                ${report.performance_indicators.strengths.map(s => `<li>${s}</li>`).join('') || '<li>No strengths identified yet</li>'}
            </ul>
        </div>
        
        <div class="report-section-content">
            <h3>📝 Recommendations</h3>
            <ul>
                ${report.recommendations.map(r => `<li>${r}</li>`).join('') || '<li>Keep up the good work!</li>'}
            </ul>
        </div>
    `;
    
    reportContent.innerHTML = html;
    reportSection.style.display = 'block';
    reportSection.scrollIntoView({ behavior: 'smooth' });
}

function closeReport() {
    document.getElementById('reportSection').style.display = 'none';
}

// Export to PDF
async function exportReportToPDF() {
    const reportContent = document.getElementById('reportContent');
    
    if (!reportContent.innerHTML) {
        showNotification('Please generate a report first!', 'warning');
        return;
    }
    
    const exportButton = document.getElementById('exportPDF');
    const originalText = exportButton.innerHTML;
    
    try {
        exportButton.innerHTML = '<span class="btn-icon">⏳</span> Exporting...';
        exportButton.disabled = true;
        
        const opt = {
            margin: 10,
            filename: `ClassAI_Report_${new Date().toISOString().split('T')[0]}.pdf`,
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };
        
        await html2pdf().set(opt).from(reportContent).save();
        
        showNotification('Report exported to PDF successfully!', 'success');
        
    } catch (error) {
        console.error('Error exporting PDF:', error);
        showNotification('Error exporting PDF: ' + error.message, 'error');
    } finally {
        exportButton.innerHTML = originalText;
        exportButton.disabled = false;
    }
}

// Notifications
function showNotification(message, type = 'info') {
    // You can implement a toast notification system here
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// Update Last Update Time
function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('lastUpdate').textContent = timeString;
}