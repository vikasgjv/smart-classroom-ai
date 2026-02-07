#!/usr/bin/env python3
"""
Student Report Generator for ClassAI
Generates comprehensive reports after class sessions
"""
import sqlite3
from datetime import datetime, timedelta
import json
import statistics
from database import SessionLocal
from models import Attention, Emotion

class StudentReportGenerator:
    def __init__(self):
        self.db = SessionLocal()
    
    def generate_session_report(self, student_id, session_start, session_end):
        """Generate comprehensive report for a class session"""
        
        # Get attention data for the session
        attention_data = self.get_attention_data(student_id, session_start, session_end)
        
        # Get emotion data for the session
        emotion_data = self.get_emotion_data(student_id, session_start, session_end)
        
        # Calculate metrics
        metrics = self.calculate_metrics(attention_data, emotion_data)
        
        # Generate insights
        insights = self.generate_insights(metrics, attention_data)
        
        # Create report structure
        report = {
            "student_info": {
                "student_id": student_id,
                "session_date": session_start.strftime("%Y-%m-%d"),
                "session_time": f"{session_start.strftime('%H:%M')} - {session_end.strftime('%H:%M')}",
                "duration_minutes": int((session_end - session_start).total_seconds() / 60)
            },
            "attention_summary": {
                "average_attention": metrics["avg_attention"],
                "peak_attention": metrics["peak_attention"],
                "lowest_attention": metrics["lowest_attention"],
                "attention_grade": metrics["attention_grade"],
                "time_highly_focused": metrics["time_high_focus"],
                "time_distracted": metrics["time_distracted"],
                "time_absent": metrics["time_absent"],
                "time_missed_minutes": metrics["time_missed_minutes"],
                "attendance_rate": metrics["attendance_rate"],
                "attention_consistency": metrics["consistency_score"]
            },
            "engagement_patterns": {
                "most_engaged_period": metrics["best_period"],
                "least_engaged_period": metrics["worst_period"],
                "attention_trend": metrics["trend"],
                "focus_drops": metrics["focus_drops"],
                "recovery_rate": metrics["recovery_rate"]
            },
            "behavioral_analysis": {
                "face_detection_rate": metrics["face_detection_rate"],
                "eye_contact_quality": metrics["eye_contact_quality"],
                "movement_patterns": metrics["movement_analysis"],
                "distraction_incidents": metrics["distraction_count"],
                "mobile_usage_rate": metrics.get("mobile_usage_rate", 0),
                "mobile_time_minutes": metrics.get("mobile_time_minutes", 0),
                "mobile_detection_count": metrics.get("mobile_detection_count", 0),
                "mobile_distraction_severity": metrics.get("mobile_distraction_severity", "No data")
            },
            "performance_indicators": {
                "overall_score": metrics["overall_score"],
                "participation_level": metrics["participation_level"],
                "learning_readiness": metrics["learning_readiness"],
                "improvement_areas": insights["improvement_areas"],
                "strengths": insights["strengths"]
            },
            "detailed_timeline": self.create_timeline(attention_data),
            "recommendations": insights["recommendations"],
            "comparative_analysis": self.get_comparative_data(student_id, metrics),
            "generated_at": datetime.now().isoformat()
        }
        
        return report
    
    def get_attention_data(self, student_id, start_time, end_time):
        """Retrieve attention data for the session"""
        records = self.db.query(Attention).filter(
            Attention.student_id == student_id,
            Attention.timestamp >= start_time,
            Attention.timestamp <= end_time
        ).order_by(Attention.timestamp).all()
        
        # Return data without mobile fields
        return [(r.timestamp, r.attention_score, False, 0.0, 0.0) for r in records]
    
    def get_emotion_data(self, student_id, start_time, end_time):
        """Retrieve emotion data for the session"""
        records = self.db.query(Emotion).filter(
            Emotion.student_id == student_id,
            Emotion.timestamp >= start_time,
            Emotion.timestamp <= end_time
        ).order_by(Emotion.timestamp).all()
        
        return [(r.timestamp, r.emotion, r.confidence) for r in records]
    
    def calculate_metrics(self, attention_data, emotion_data):
        """Calculate comprehensive metrics from the data"""
        if not attention_data:
            return self.get_empty_metrics()
        
        scores = [score for _, score, _, _, _ in attention_data]
        
        # Basic statistics
        avg_attention = round(statistics.mean(scores) * 100, 1)
        peak_attention = round(max(scores) * 100, 1)
        lowest_attention = round(min(scores) * 100, 1)
        
        # Attention grade
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
        
        # Time analysis
        total_readings = len(scores)
        high_focus_count = sum(1 for score in scores if score >= 0.8)
        distracted_count = sum(1 for score in scores if score < 0.5)
        absent_count = sum(1 for score in scores if score <= 0.2)
        
        # Attention grade
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
        
        # Time analysis
        high_focus_count = sum(1 for score in scores if score >= 0.8)
        distracted_count = sum(1 for score in scores if score < 0.5)
        absent_count = sum(1 for score in scores if score <= 0.2)  # No face detected
        
        time_high_focus = round((high_focus_count / total_readings) * 100, 1) if total_readings > 0 else 0
        time_distracted = round((distracted_count / total_readings) * 100, 1) if total_readings > 0 else 0
        time_absent = round((absent_count / total_readings) * 100, 1) if total_readings > 0 else 0
        
        # Calculate actual time missed in minutes (estimate session duration from data)
        if len(attention_data) > 1:
            session_duration = (attention_data[-1][0] - attention_data[0][0]).total_seconds() / 60
        else:
            session_duration = total_readings * 3 / 60  # Assume 3-second intervals
        
        time_missed_minutes = round((absent_count / total_readings) * session_duration, 1) if total_readings > 0 else 0
        
        # Consistency (lower standard deviation = more consistent)
        consistency = round(100 - (statistics.stdev(scores) * 100), 1) if len(scores) > 1 else 100
        
        # Trend analysis
        if len(scores) >= 3:
            first_third = statistics.mean(scores[:len(scores)//3])
            last_third = statistics.mean(scores[-len(scores)//3:])
            trend = "Improving" if last_third > first_third + 0.1 else "Declining" if last_third < first_third - 0.1 else "Stable"
        else:
            trend = "Insufficient data"
        
        # Find best and worst periods
        best_period, worst_period = self.find_attention_periods(attention_data)
        
        # Count focus drops (attention drops > 20% between readings)
        focus_drops = 0
        for i in range(1, len(scores)):
            if scores[i-1] - scores[i] > 0.2:
                focus_drops += 1
        
        # Recovery rate (how quickly attention recovers after drops)
        recovery_rate = self.calculate_recovery_rate(scores)
        
        # Face detection rate
        face_detection_rate = round((sum(1 for score in scores if score > 0.2) / total_readings) * 100, 1)
        
        # Overall score (weighted combination, no mobile penalty)
        overall_score = round(
            (avg_attention * 0.4) + 
            (consistency * 0.2) + 
            (time_high_focus * 0.2) + 
            (face_detection_rate * 0.2), 1
        )
        overall_score = max(0, overall_score)
        
        # Calculate attendance rate
        attendance_rate = round(100 - time_absent, 1)
        
        return {
            "avg_attention": avg_attention,
            "peak_attention": peak_attention,
            "lowest_attention": lowest_attention,
            "attention_grade": grade,
            "time_high_focus": time_high_focus,
            "time_distracted": time_distracted,
            "time_absent": time_absent,
            "time_missed_minutes": time_missed_minutes,
            "attendance_rate": attendance_rate,
            "consistency_score": consistency,
            "trend": trend,
            "best_period": best_period,
            "worst_period": worst_period,
            "focus_drops": focus_drops,
            "recovery_rate": recovery_rate,
            "face_detection_rate": face_detection_rate,
            "eye_contact_quality": self.assess_eye_contact(scores),
            "movement_analysis": self.analyze_movement(scores),
            "distraction_count": distracted_count,
            "overall_score": overall_score,
            "participation_level": self.assess_participation(avg_attention),
            "learning_readiness": self.assess_learning_readiness(avg_attention, consistency),
            "mobile_usage_rate": 0,
            "mobile_time_minutes": 0,
            "mobile_detection_count": 0,
            "avg_mobile_confidence": 0,
            "mobile_distraction_severity": "No mobile detection"
        }
    
    def generate_insights(self, metrics, attention_data):
        """Generate insights and recommendations"""
        strengths = []
        improvement_areas = []
        recommendations = []
        
        # Analyze strengths
        if metrics["avg_attention"] >= 75:
            strengths.append("Maintains high average attention throughout class")
        if metrics["consistency_score"] >= 80:
            strengths.append("Shows consistent focus levels")
        if metrics["time_high_focus"] >= 60:
            strengths.append("Spends majority of time in high focus state")
        if metrics["recovery_rate"] >= 70:
            strengths.append("Quickly recovers from attention drops")
        if metrics["attendance_rate"] >= 90:
            strengths.append("Excellent class attendance and presence")
        
        # Identify improvement areas
        if metrics["avg_attention"] < 60:
            improvement_areas.append("Overall attention level needs improvement")
            recommendations.append("Consider shorter study sessions with breaks")
        if metrics["time_distracted"] > 30:
            improvement_areas.append("Frequent distraction periods")
            recommendations.append("Identify and minimize environmental distractions")
        if metrics["time_absent"] > 20:
            improvement_areas.append(f"Missed {metrics['time_missed_minutes']} minutes of class (not present)")
            recommendations.append("Improve attendance and stay present during entire class")
        if metrics["focus_drops"] > len(attention_data) * 0.3:
            improvement_areas.append("Attention drops frequently during class")
            recommendations.append("Practice attention-building exercises")
        if metrics["consistency_score"] < 60:
            improvement_areas.append("Inconsistent attention patterns")
            recommendations.append("Develop regular study routines")
        
        # Trend-based recommendations
        if metrics["trend"] == "Declining":
            recommendations.append("Take more frequent breaks to maintain focus")
        elif metrics["trend"] == "Improving":
            recommendations.append("Continue current engagement strategies")
        
        # Time-based recommendations
        if metrics["worst_period"]:
            recommendations.append(f"Pay special attention during {metrics['worst_period']} period")
        
        return {
            "strengths": strengths,
            "improvement_areas": improvement_areas,
            "recommendations": recommendations
        }
    
    def create_timeline(self, attention_data):
        """Create detailed timeline of attention levels"""
        timeline = []
        for timestamp, score, mobile_detected, mobile_confidence, distraction_level in attention_data:
            timeline.append({
                "time": timestamp.strftime("%H:%M:%S"),
                "attention_percent": round(score * 100, 1),
                "level": self.get_attention_level(score),
                "status": self.get_status_description(score),
                "mobile_detected": mobile_detected,
                "mobile_confidence": round(mobile_confidence, 2) if mobile_confidence else 0
            })
        return timeline
    
    def get_attention_level(self, score):
        """Convert score to attention level"""
        if score >= 0.8:
            return "High"
        elif score >= 0.5:
            return "Medium"
        else:
            return "Low"
    
    def get_status_description(self, score):
        """Get descriptive status for attention score"""
        if score >= 0.8:
            return "Highly focused and engaged"
        elif score >= 0.6:
            return "Good attention level"
        elif score >= 0.4:
            return "Moderate attention"
        elif score >= 0.2:
            return "Low attention, some distraction"
        else:
            return "Very low attention or not present"
    
    def find_attention_periods(self, attention_data):
        """Find best and worst 5-minute periods"""
        if len(attention_data) < 5:
            return None, None
        
        # Group into 5-minute windows
        windows = []
        for i in range(0, len(attention_data) - 4):
            # Extract just the timestamp and score from the tuple
            window_scores = [score for _, score, _, _, _ in attention_data[i:i+5]]
            avg_score = statistics.mean(window_scores)
            start_time = attention_data[i][0].strftime("%H:%M")
            windows.append((start_time, avg_score))
        
        if windows:
            best = max(windows, key=lambda x: x[1])
            worst = min(windows, key=lambda x: x[1])
            return best[0], worst[0]
        
        return None, None
    
    def calculate_recovery_rate(self, scores):
        """Calculate how quickly attention recovers after drops"""
        recoveries = []
        for i in range(1, len(scores) - 1):
            if scores[i] < scores[i-1] - 0.2:  # Attention drop
                # Look for recovery in next few readings
                for j in range(i+1, min(i+4, len(scores))):
                    if scores[j] > scores[i] + 0.1:  # Recovery
                        recoveries.append(j - i)
                        break
        
        if recoveries:
            avg_recovery_time = statistics.mean(recoveries)
            return round(100 - (avg_recovery_time * 20), 1)  # Convert to percentage
        return 50  # Default if no clear patterns
    
    def assess_eye_contact(self, scores):
        """Assess eye contact quality based on attention scores"""
        high_attention_ratio = sum(1 for score in scores if score >= 0.7) / len(scores)
        if high_attention_ratio >= 0.8:
            return "Excellent eye contact"
        elif high_attention_ratio >= 0.6:
            return "Good eye contact"
        elif high_attention_ratio >= 0.4:
            return "Moderate eye contact"
        else:
            return "Poor eye contact"
    
    def analyze_movement(self, scores):
        """Analyze movement patterns from attention variations"""
        if len(scores) < 3:
            return "Insufficient data"
        
        variations = [abs(scores[i] - scores[i-1]) for i in range(1, len(scores))]
        avg_variation = statistics.mean(variations)
        
        if avg_variation < 0.1:
            return "Very stable positioning"
        elif avg_variation < 0.2:
            return "Stable with minor movements"
        elif avg_variation < 0.3:
            return "Moderate movement"
        else:
            return "High movement/fidgeting"
    
    def assess_participation(self, avg_attention):
        """Assess participation level"""
        if avg_attention >= 80:
            return "Highly Engaged"
        elif avg_attention >= 65:
            return "Actively Participating"
        elif avg_attention >= 50:
            return "Moderately Engaged"
        else:
            return "Passive/Disengaged"
    
    def assess_learning_readiness(self, avg_attention, consistency):
        """Assess readiness for learning"""
        combined_score = (avg_attention + consistency) / 2
        if combined_score >= 80:
            return "Optimal learning state"
        elif combined_score >= 65:
            return "Good learning readiness"
        elif combined_score >= 50:
            return "Adequate for learning"
        else:
            return "Suboptimal learning conditions"
    
    def assess_mobile_distraction(self, mobile_usage_rate, avg_mobile_confidence):
        """Assess the severity of mobile phone distraction"""
        if mobile_usage_rate == 0:
            return "No mobile usage detected"
        elif mobile_usage_rate <= 10:
            return "Minimal mobile usage"
        elif mobile_usage_rate <= 25:
            return "Moderate mobile distraction"
        elif mobile_usage_rate <= 50:
            return "High mobile distraction"
        else:
            return "Severe mobile addiction - immediate intervention needed"
    
    def get_comparative_data(self, student_id, current_metrics):
        """Get comparative data from previous sessions"""
        # This would compare with historical data
        # For now, return placeholder
        return {
            "previous_sessions": 0,
            "improvement_trend": "First session - no comparison available",
            "class_average": "Not available",
            "ranking": "Not available"
        }
    
    def get_empty_metrics(self):
        """Return empty metrics when no data available"""
        return {
            "avg_attention": 0,
            "peak_attention": 0,
            "lowest_attention": 0,
            "attention_grade": "No Data",
            "time_high_focus": 0,
            "time_distracted": 0,
            "time_absent": 0,
            "time_missed_minutes": 0,
            "attendance_rate": 0,
            "consistency_score": 0,
            "trend": "No data",
            "best_period": None,
            "worst_period": None,
            "focus_drops": 0,
            "recovery_rate": 0,
            "face_detection_rate": 0,
            "eye_contact_quality": "No data",
            "movement_analysis": "No data",
            "distraction_count": 0,
            "overall_score": 0,
            "participation_level": "No data",
            "learning_readiness": "No data",
            "mobile_usage_rate": 0,
            "mobile_time_minutes": 0,
            "mobile_detection_count": 0,
            "avg_mobile_confidence": 0,
            "mobile_distraction_severity": "No data"
        }
    
    def save_report_to_file(self, report, filename=None):
        """Save report to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            student_id = report["student_info"]["student_id"]
            filename = f"report_{student_id}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filename
    
    def generate_html_report(self, report):
        """Generate HTML version of the report"""
        html_template = """<!DOCTYPE html>
<html>
<head>
    <title>ClassAI Student Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #e9ecef; border-radius: 5px; }}
        .grade-A {{ color: #28a745; font-weight: bold; }}
        .grade-B {{ color: #17a2b8; font-weight: bold; }}
        .grade-C {{ color: #ffc107; font-weight: bold; }}
        .grade-D {{ color: #fd7e14; font-weight: bold; }}
        .grade-F {{ color: #dc3545; font-weight: bold; }}
        .absence {{ color: #dc3545; font-weight: bold; }}
        .mobile-warning {{ color: #dc3545; font-weight: bold; background: #f8d7da; }}
        .mobile-moderate {{ color: #856404; font-weight: bold; background: #fff3cd; }}
        .mobile-good {{ color: #155724; font-weight: bold; background: #d4edda; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>ClassAI Student Report</h1>
        <p><strong>Student:</strong> {student_id}</p>
        <p><strong>Date:</strong> {session_date}</p>
        <p><strong>Duration:</strong> {duration} minutes</p>
    </div>
    
    <div class="section">
        <h2>Attention Summary</h2>
        <div class="metric">Average Attention: <strong>{avg_attention}%</strong></div>
        <div class="metric">Grade: <span class="grade-{grade_class}">{grade}</span></div>
        <div class="metric">Peak Attention: <strong>{peak_attention}%</strong></div>
        <div class="metric">Overall Score: <strong>{overall_score}/100</strong></div>
    </div>
    
    <div class="section">
        <h2>Attendance & Presence</h2>
        <div class="metric">Attendance Rate: <strong>{attendance_rate}%</strong></div>
        <div class="metric absence">Time Missed: <strong>{time_missed} minutes</strong></div>
        <div class="metric">Time Absent: <strong>{time_absent}%</strong></div>
    </div>
    
    <div class="section">
        <h2>Mobile Phone Usage Analysis</h2>
        <div class="metric {mobile_class}">Usage Rate: <strong>{mobile_usage_rate}%</strong></div>
        <div class="metric {mobile_class}">Time on Phone: <strong>{mobile_time} minutes</strong></div>
        <div class="metric">Detection Count: <strong>{mobile_count} instances</strong></div>
        <div class="metric">Usage Status: <strong>{mobile_status}</strong></div>
        <div class="metric">Impact Assessment: <strong>{mobile_severity}</strong></div>
    </div>
    
    <div class="section">
        <h2>Performance Indicators</h2>
        <p><strong>Participation Level:</strong> {participation}</p>
        <p><strong>Learning Readiness:</strong> {learning_readiness}</p>
        <p><strong>Eye Contact Quality:</strong> {eye_contact}</p>
    </div>
    
    <div class="section">
        <h2>Strengths</h2>
        <ul>{strengths}</ul>
    </div>
    
    <div class="section">
        <h2>Areas for Improvement</h2>
        <ul>{improvement_areas}</ul>
    </div>
    
    <div class="section">
        <h2>Recommendations</h2>
        <ul>{recommendations}</ul>
    </div>
</body>
</html>"""
        
        # Format the HTML
        grade_class = report["attention_summary"]["attention_grade"].split(" - ")[0]
        
        # Determine mobile usage status
        mobile_rate = report["behavioral_analysis"]["mobile_usage_rate"]
        mobile_count = report["behavioral_analysis"]["mobile_detection_count"]
        
        if mobile_rate == 0:
            mobile_class = "mobile-good"
            mobile_status = "No phone usage detected"
        elif mobile_rate <= 5:
            mobile_class = "mobile-good"
            mobile_status = "Excellent digital discipline"
        elif mobile_rate <= 15:
            mobile_class = "mobile-moderate"
            mobile_status = "Minor phone usage"
        elif mobile_rate <= 30:
            mobile_class = "mobile-warning"
            mobile_status = "Moderate phone distraction"
        else:
            mobile_class = "mobile-warning"
            mobile_status = "Excessive phone usage - needs attention"
        
        # Format lists
        recommendations_html = "".join([f"<li>{rec}</li>" for rec in report["recommendations"]])
        strengths_html = "".join([f"<li>{strength}</li>" for strength in report["performance_indicators"]["strengths"]])
        improvement_html = "".join([f"<li>{area}</li>" for area in report["performance_indicators"]["improvement_areas"]])
        
        html_content = html_template.format(
            student_id=report["student_info"]["student_id"],
            session_date=report["student_info"]["session_date"],
            duration=report["student_info"]["duration_minutes"],
            avg_attention=report["attention_summary"]["average_attention"],
            grade=report["attention_summary"]["attention_grade"],
            grade_class=grade_class,
            peak_attention=report["attention_summary"]["peak_attention"],
            overall_score=report["performance_indicators"]["overall_score"],
            attendance_rate=report["attention_summary"]["attendance_rate"],
            time_missed=report["attention_summary"]["time_missed_minutes"],
            time_absent=report["attention_summary"]["time_absent"],
            mobile_usage_rate=report["behavioral_analysis"]["mobile_usage_rate"],
            mobile_time=report["behavioral_analysis"]["mobile_time_minutes"],
            mobile_count=report["behavioral_analysis"]["mobile_detection_count"],
            mobile_status=mobile_status,
            mobile_severity=report["behavioral_analysis"]["mobile_distraction_severity"],
            mobile_class=mobile_class,
            participation=report["performance_indicators"]["participation_level"],
            learning_readiness=report["performance_indicators"]["learning_readiness"],
            eye_contact=report["behavioral_analysis"]["eye_contact_quality"],
            recommendations=recommendations_html,
            strengths=strengths_html,
            improvement_areas=improvement_html
        )
        
        return html_content

# Example usage function
def generate_sample_report():
    """Generate a sample report for testing"""
    generator = StudentReportGenerator()
    
    # Sample session times
    session_start = datetime.now() - timedelta(hours=1)
    session_end = datetime.now()
    
    report = generator.generate_session_report("S01", session_start, session_end)
    
    # Save JSON report
    json_file = generator.save_report_to_file(report)
    print(f"JSON report saved: {json_file}")
    
    # Generate HTML report
    html_content = generator.generate_html_report(report)
    html_file = json_file.replace('.json', '.html')
    with open(html_file, 'w') as f:
        f.write(html_content)
    print(f"HTML report saved: {html_file}")
    
    return report

if __name__ == "__main__":
    report = generate_sample_report()
    print("\nSample Report Generated!")
    print(f"Overall Score: {report['performance_indicators']['overall_score']}/100")
    print(f"Attention Grade: {report['attention_summary']['attention_grade']}")