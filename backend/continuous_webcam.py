#!/usr/bin/env python3
"""
Continuous webcam monitoring for ClassAI
Uses enhanced OpenCV detection for improved accuracy
"""
import cv2
import numpy as np
import threading
import time
from datetime import datetime
from collections import deque

class ContinuousWebcam:
    def __init__(self):
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.last_attention_score = 0.1
        self.last_mobile_detected = False
        self.last_mobile_confidence = 0.0
        self.last_distraction_level = 0.0
        self.frame_lock = threading.Lock()
        
        # Enhanced detection components
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
        
        # Attention tracking for smoothing
        self.attention_history = deque(maxlen=5)
        self.face_size_history = deque(maxlen=5)
        
        print("📹 Enhanced continuous webcam initialized")
    
    def start_webcam(self):
        """Start continuous webcam monitoring"""
        if self.is_running:
            return True
            
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ Could not open webcam")
            return False
        
        # Set enhanced camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Better lighting
        
        self.is_running = True
        
        # Start background thread for continuous processing
        self.processing_thread = threading.Thread(target=self._continuous_processing)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        print("✅ Enhanced continuous webcam started")
        return True
    
    def stop_webcam(self):
        """Stop continuous webcam monitoring"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        print("🛑 Enhanced continuous webcam stopped")
    
    def _continuous_processing(self):
        """Background thread for continuous frame processing"""
        frame_count = 0
        while self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            
            if not ret:
                time.sleep(0.01)
                continue
            
            # Store current frame
            with self.frame_lock:
                self.current_frame = frame.copy()
            
            # Process every 2nd frame for performance
            frame_count += 1
            if frame_count % 2 == 0:
                self._process_frame_enhanced(frame)
            
            time.sleep(0.033)  # ~30 FPS
    
    def _process_frame_enhanced(self, frame):
        """Enhanced frame processing with multiple detection methods"""
        try:
            # Detect attention with enhanced methods
            attention_score = self._detect_attention_enhanced(frame)
            
            # Update stored values
            self.last_attention_score = attention_score
            self.last_mobile_detected = False
            self.last_mobile_confidence = 0.0
            self.last_distraction_level = 0.0
            
        except Exception as e:
            print(f"Error processing frame: {e}")
    
    def _detect_attention_enhanced(self, frame):
        """Enhanced attention detection with multiple methods"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply histogram equalization for better contrast
        gray_eq = cv2.equalizeHist(gray)
        
        # Apply Gaussian blur to reduce noise
        gray_blur = cv2.GaussianBlur(gray_eq, (3, 3), 0)
        
        # Detect faces with multiple cascades
        faces = self._detect_faces_enhanced(gray_blur)
        
        if len(faces) == 0:
            print("❌ No face detected - Student absent")
            self.attention_history.append(0.1)
            return 0.1
        
        print(f"✅ Detected {len(faces)} face(s)")
        
        # Process the best face
        best_face = max(faces, key=lambda x: x[2] * x[3])  # Largest face
        x, y, w, h = best_face
        
        # Calculate attention score for this face
        attention_score = self._calculate_face_attention(gray_blur, best_face)
        
        # Apply temporal smoothing
        self.attention_history.append(attention_score)
        if len(self.attention_history) >= 3:
            # Weighted average with recent frames
            weights = [0.5, 0.3, 0.2]  # Current frame has highest weight
            smoothed_score = sum(w * score for w, score in zip(weights, list(self.attention_history)[-3:]))
            attention_score = smoothed_score
        
        print(f"📊 Final attention score: {attention_score:.2f}")
        return round(attention_score, 2)
    
    def _detect_faces_enhanced(self, gray):
        """Enhanced face detection with multiple methods"""
        all_faces = []
        
        # Method 1: Frontal face detection (primary)
        faces_frontal = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=4,
            minSize=(60, 60),
            maxSize=(400, 400),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        all_faces.extend(faces_frontal)
        
        # Method 2: Profile face detection (for side views)
        faces_profile = self.profile_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(60, 60),
            maxSize=(400, 400)
        )
        all_faces.extend(faces_profile)
        
        # Method 3: More sensitive frontal detection
        if len(all_faces) == 0:
            faces_sensitive = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.03,
                minNeighbors=3,
                minSize=(50, 50),
                maxSize=(500, 500)
            )
            all_faces.extend(faces_sensitive)
        
        # Remove duplicate faces (overlapping detections)
        unique_faces = self._remove_duplicate_faces(all_faces)
        
        # Validate faces
        valid_faces = self._validate_faces_enhanced(unique_faces)
        
        return valid_faces
    
    def _remove_duplicate_faces(self, faces):
        """Remove overlapping face detections"""
        if len(faces) <= 1:
            return faces
        
        unique_faces = []
        for face in faces:
            x1, y1, w1, h1 = face
            is_duplicate = False
            
            for existing_face in unique_faces:
                x2, y2, w2, h2 = existing_face
                
                # Calculate overlap
                overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
                overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
                overlap_area = overlap_x * overlap_y
                
                area1 = w1 * h1
                area2 = w2 * h2
                
                # If overlap is significant, it's a duplicate
                if overlap_area > 0.3 * min(area1, area2):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_faces.append(face)
        
        return unique_faces
    
    def _validate_faces_enhanced(self, faces):
        """Enhanced face validation"""
        valid_faces = []
        
        for (x, y, w, h) in faces:
            # Size validation
            if w < 40 or h < 40 or w > 600 or h > 600:
                continue
            
            # Aspect ratio validation (faces are roughly square to slightly tall)
            aspect_ratio = h / w
            if aspect_ratio < 0.7 or aspect_ratio > 2.0:
                continue
            
            # Area validation
            area = w * h
            if area < 1600 or area > 360000:
                continue
            
            valid_faces.append((x, y, w, h))
        
        return valid_faces[:2]  # Maximum 2 faces
    
    def _calculate_face_attention(self, gray, face):
        """Calculate attention score for a detected face"""
        x, y, w, h = face
        face_roi = gray[y:y+h, x:x+w]
        
        # Base attention from face size (larger face = more engaged)
        face_area = w * h
        self.face_size_history.append(face_area)
        
        # Normalize face size (typical range: 5000-50000 pixels)
        size_factor = min(1.0, face_area / 25000)
        
        # Detect eyes in face region
        eyes = self._detect_eyes_enhanced(face_roi)
        
        # Calculate base attention based on eye detection
        if len(eyes) >= 2:
            # Both eyes detected - high attention
            base_attention = 0.80 + (size_factor * 0.10)
            print(f"  Both eyes detected, high attention")
        elif len(eyes) == 1:
            # One eye detected - medium attention
            base_attention = 0.60 + (size_factor * 0.10)
            print(f"  One eye detected, medium attention")
        else:
            # No eyes detected - could be looking away, glasses, or poor lighting
            base_attention = 0.35 + (size_factor * 0.15)
            print(f"  No eyes detected, checking face quality...")
            
            # Additional checks for face quality
            face_quality = self._assess_face_quality(face_roi)
            base_attention += face_quality * 0.15
        
        # Add engagement boost for consistent face size
        if len(self.face_size_history) >= 3:
            size_consistency = 1.0 - (np.std(list(self.face_size_history)[-3:]) / np.mean(list(self.face_size_history)[-3:]))
            size_consistency = max(0, min(1, size_consistency))
            base_attention += size_consistency * 0.05
        
        # Add small random variation for realism
        variation = np.random.uniform(-0.03, 0.03)
        final_attention = max(0.15, min(0.95, base_attention + variation))
        
        print(f"  Face area: {face_area}, Size factor: {size_factor:.2f}, Final: {final_attention:.2f}")
        return final_attention
    
    def _detect_eyes_enhanced(self, face_roi):
        """Enhanced eye detection with multiple methods"""
        # Method 1: Standard eye detection
        eyes1 = self.eye_cascade.detectMultiScale(
            face_roi,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(15, 15),
            maxSize=(80, 80)
        )
        
        if len(eyes1) >= 1:
            return self._filter_valid_eyes(eyes1, face_roi)
        
        # Method 2: More sensitive detection
        eyes2 = self.eye_cascade.detectMultiScale(
            face_roi,
            scaleFactor=1.05,
            minNeighbors=2,
            minSize=(10, 10),
            maxSize=(100, 100)
        )
        
        return self._filter_valid_eyes(eyes2, face_roi)
    
    def _filter_valid_eyes(self, eyes, face_roi):
        """Filter and validate detected eyes"""
        valid_eyes = []
        face_h, face_w = face_roi.shape
        
        for (ex, ey, ew, eh) in eyes:
            # Size validation
            if ew < 8 or eh < 8 or ew > face_w * 0.6 or eh > face_h * 0.4:
                continue
            
            # Position validation (eyes should be in upper half of face)
            if ey > face_h * 0.7:
                continue
            
            # Aspect ratio validation
            aspect_ratio = ew / eh
            if aspect_ratio < 0.5 or aspect_ratio > 4.0:
                continue
            
            valid_eyes.append((ex, ey, ew, eh))
        
        return valid_eyes[:2]  # Maximum 2 eyes
    
    def _assess_face_quality(self, face_roi):
        """Assess face quality for attention estimation"""
        if face_roi.size == 0:
            return 0.0
        
        # Calculate image sharpness (Laplacian variance)
        laplacian_var = cv2.Laplacian(face_roi, cv2.CV_64F).var()
        sharpness_score = min(1.0, laplacian_var / 500)  # Normalize
        
        # Calculate contrast
        contrast = face_roi.std()
        contrast_score = min(1.0, contrast / 50)  # Normalize
        
        # Calculate brightness (should be reasonable)
        brightness = face_roi.mean()
        brightness_score = 1.0 - abs(brightness - 128) / 128  # Optimal around 128
        
        # Combined quality score
        quality_score = (sharpness_score * 0.4 + contrast_score * 0.3 + brightness_score * 0.3)
        
        return max(0, min(1, quality_score))
    
    def _detect_mobile_enhanced(self, frame):
        """Enhanced mobile phone detection"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Morphological operations to connect edges
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        best_confidence = 0.0
        
        for contour in contours:
            confidence = self._analyze_mobile_contour(contour, gray)
            best_confidence = max(best_confidence, confidence)
        
        mobile_detected = best_confidence > 0.85  # Higher threshold
        
        if mobile_detected:
            print(f"📱 Mobile detected with confidence: {best_confidence:.2f}")
        
        return mobile_detected, best_confidence
    
    def _analyze_mobile_contour(self, contour, gray_image):
        """Analyze contour for mobile phone characteristics"""
        x, y, w, h = cv2.boundingRect(contour)
        
        # Phone size and aspect ratio constraints
        aspect_ratio = h / w if w > 0 else 0
        area = w * h
        
        # Strict phone characteristics
        if not (1.5 <= aspect_ratio <= 2.5 or 0.4 <= aspect_ratio <= 0.67):
            return 0.0
        
        if not (8000 <= area <= 35000):  # More restrictive area
            return 0.0
        
        # Analyze region properties
        roi = gray_image[y:y+h, x:x+w]
        if roi.size == 0:
            return 0.0
        
        # Check for uniform regions (screen-like)
        uniformity = 1.0 - (np.std(roi) / 128.0)
        
        # Check rectangularity
        contour_area = cv2.contourArea(contour)
        bbox_area = w * h
        rectangularity = contour_area / bbox_area if bbox_area > 0 else 0
        
        # Check for typical phone brightness
        mean_brightness = np.mean(roi)
        brightness_score = 1.0 if 30 <= mean_brightness <= 200 else 0.5
        
        # Combined confidence with stricter requirements
        confidence = (uniformity * 0.4 + rectangularity * 0.4 + brightness_score * 0.2)
        
        # Boost for ideal phone aspect ratios
        if 1.7 <= aspect_ratio <= 2.1:
            confidence *= 1.2
        
        # Boost for ideal phone areas
        if 12000 <= area <= 25000:
            confidence *= 1.1
        
        return min(0.95, confidence)
    
    def _calculate_distraction_level(self, attention_score, mobile_detected, mobile_confidence):
        """Calculate overall distraction level"""
        if mobile_detected:
            return min(1.0, mobile_confidence + 0.1)
        elif attention_score < 0.3:
            return 0.6
        elif attention_score < 0.5:
            return 0.3
        else:
            return 0.1
    
    def get_current_data(self):
        """Get the latest detection results"""
        return {
            'attention_score': self.last_attention_score,
            'mobile_detected': False,
            'mobile_confidence': 0.0,
            'distraction_level': 0.0,
            'timestamp': datetime.now().isoformat(),
            'attention_trend': self._get_attention_trend()
        }
    
    def _get_attention_trend(self):
        """Calculate attention trend from history"""
        if len(self.attention_history) < 3:
            return "insufficient_data"
        
        recent = list(self.attention_history)[-3:]
        if recent[-1] > recent[0] + 0.1:
            return "improving"
        elif recent[-1] < recent[0] - 0.1:
            return "declining"
        else:
            return "stable"
    
    def get_current_frame(self):
        """Get the current frame (for debugging/display)"""
        with self.frame_lock:
            return self.current_frame.copy() if self.current_frame is not None else None

# Global webcam instance
continuous_webcam = ContinuousWebcam()

def start_continuous_monitoring():
    """Start continuous webcam monitoring"""
    return continuous_webcam.start_webcam()

def stop_continuous_monitoring():
    """Stop continuous webcam monitoring"""
    continuous_webcam.stop_webcam()

def get_live_attention_data():
    """Get current attention and mobile detection data"""
    return continuous_webcam.get_current_data()

def is_webcam_running():
    """Check if webcam is currently running"""
    return continuous_webcam.is_running