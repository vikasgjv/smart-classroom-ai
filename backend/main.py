from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from models import Emotion, Attention, Base
from ai_attention import detect_attention
from continuous_webcam import start_continuous_monitoring, stop_continuous_monitoring, get_live_attention_data, is_webcam_running
from ai_engagement import engagement
from report_generator import StudentReportGenerator
import numpy as np
from datetime import datetime

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "ClassAI backend is running"}

@app.get("/student")
def get_student():
    return {
        "student_id": "S01",
        "name": "Rahul",
        "emotion": "focused",
        "attention_score": 0.87
    }

@app.post("/emotion")
def detect_emotion(data: dict):
    db = SessionLocal()

    emotion = Emotion(
        student_id=data.get("student_id"),
        emotion="happy",
        confidence=0.91
    )

    db.add(emotion)
    db.commit()
    db.refresh(emotion)
    db.close()

    return {
        "message": "Emotion saved successfully",
        "id": emotion.id,
        "student_id": emotion.student_id,
        "emotion": emotion.emotion,
        "confidence": emotion.confidence
    }



@app.get("/emotions")
def get_emotions():
    db = SessionLocal()
    emotions = db.query(Emotion).all()
    db.close()
    return emotions


@app.post("/attention")
def track_attention(data: dict):
    score = detect_attention("sample.jpg")

    db = SessionLocal()
    record = Attention(
        student_id=data.get("student_id"),
        attention_score=score
    )

    db.add(record)
    db.commit()
    db.close()

    return {
        "student_id": data.get("student_id"),
        "attention_score": score
    }



@app.get("/emotions/{student_id}")
def get_emotions_by_student(student_id: str):
    db = SessionLocal()
    data = db.query(Emotion).filter(Emotion.student_id == student_id).all()
    db.close()
    return data

@app.post("/start-monitoring")
def start_monitoring():
    """Start continuous webcam monitoring"""
    success = start_continuous_monitoring()
    return {
        "status": "success" if success else "error",
        "message": "Continuous monitoring started" if success else "Failed to start webcam",
        "webcam_running": is_webcam_running()
    }

@app.post("/stop-monitoring")
def stop_monitoring():
    """Stop continuous webcam monitoring"""
    stop_continuous_monitoring()
    return {
        "status": "success",
        "message": "Continuous monitoring stopped",
        "webcam_running": is_webcam_running()
    }

@app.get("/monitoring-status")
def monitoring_status():
    """Get current monitoring status"""
    return {
        "webcam_running": is_webcam_running(),
        "status": "active" if is_webcam_running() else "inactive"
    }

@app.post("/live-attention")
def live_attention(data: dict):
    """Get live attention score from continuous webcam monitoring"""
    try:
        # Get data from continuous monitoring
        live_data = get_live_attention_data()
        
        attention_score = live_data['attention_score']
        mobile_detected = live_data['mobile_detected']
        mobile_confidence = live_data['mobile_confidence']
        distraction_level = live_data['distraction_level']
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        db = SessionLocal()
        record = Attention(
            student_id=data.get("student_id", "unknown"),
            attention_score=attention_score,
            mobile_detected=False,
            mobile_confidence=0.0,
            distraction_level=0.0
        )
        db.add(record)
        db.commit()
        db.close()

        # Determine detection status with improved logic
        if attention_score <= 0.2:
            detection_status = "no_face_detected"
        elif attention_score <= 0.5:
            detection_status = "face_detected_low_attention"
        else:
            detection_status = "face_detected_high_attention"

        return {
            "student_id": data.get("student_id", "unknown"),
            "live_attention_score": attention_score,
            "mobile_detected": False,
            "mobile_confidence": 0.0,
            "distraction_level": 0.0,
            "status": "success",
            "timestamp": timestamp,
            "detection_status": detection_status,
            "webcam_running": is_webcam_running()
        }
    except Exception as e:
        print(f"Error in live attention: {e}")
        return {
            "student_id": data.get("student_id", "unknown"),
            "live_attention_score": 0.1,
            "mobile_detected": False,
            "mobile_confidence": 0.0,
            "distraction_level": 0.0,
            "status": "error",
            "message": str(e),
            "webcam_running": is_webcam_running()
        }

@app.post("/generate-report")
def generate_student_report(data: dict):
    """Generate comprehensive student report for a session"""
    try:
        student_id = data.get("student_id", "S01")
        
        # Get session times (default to last hour if not provided)
        if "session_start" in data and "session_end" in data:
            session_start = datetime.fromisoformat(data["session_start"])
            session_end = datetime.fromisoformat(data["session_end"])
        else:
            # Default to last hour
            session_end = datetime.now()
            session_start = session_end.replace(hour=session_end.hour-1) if session_end.hour > 0 else session_end.replace(hour=23, day=session_end.day-1)
        
        # Generate report
        generator = StudentReportGenerator()
        report = generator.generate_session_report(student_id, session_start, session_end)
        
        # Save report files
        json_file = generator.save_report_to_file(report)
        
        html_content = generator.generate_html_report(report)
        html_file = json_file.replace('.json', '.html')
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return {
            "status": "success",
            "report": report,
            "files": {
                "json_report": json_file,
                "html_report": html_file
            },
            "summary": {
                "overall_score": report["performance_indicators"]["overall_score"],
                "attention_grade": report["attention_summary"]["attention_grade"],
                "average_attention": report["attention_summary"]["average_attention"],
                "recommendations_count": len(report["recommendations"])
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "report": None
        }

@app.get("/report-preview/{student_id}")
def get_report_preview(student_id: str):
    """Get a quick preview of student performance"""
    try:
        # Get recent attention data (last 30 records)
        db = SessionLocal()
        recent_data = db.query(Attention).filter(
            Attention.student_id == student_id
        ).order_by(Attention.timestamp.desc()).limit(30).all()
        db.close()
        
        if not recent_data:
            return {"status": "no_data", "message": "No attention data found"}
        
        # Calculate quick metrics
        scores = [r.attention_score for r in recent_data]
        avg_attention = round(sum(scores) / len(scores) * 100, 1)
        
        # Determine grade
        if avg_attention >= 80:
            grade = "A - Excellent"
        elif avg_attention >= 70:
            grade = "B - Good"
        elif avg_attention >= 60:
            grade = "C - Average"
        elif avg_attention >= 50:
            grade = "D - Below Average"
        else:
            grade = "F - Needs Improvement"
        
        return {
            "status": "success",
            "student_id": student_id,
            "recent_sessions": len(recent_data),
            "average_attention": avg_attention,
            "grade": grade,
            "last_session": recent_data[0].timestamp.isoformat(),
            "trend": "Improving" if len(scores) > 1 and scores[0] > scores[-1] else "Stable"
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/engagement")
def engagement_score(data: dict):
    score = engagement(
        attention=data.get("attention"),
        emotion=data.get("emotion")
    )

    return {
        "student_id": data.get("student_id"),
        "engagement_score": score
    }
