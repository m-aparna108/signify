import cv2
import os
import sys
import time
from flask import Response

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml_model.hand_detection import detect_hands
from ml_model.keypoint_classifier import KeyPointClassifier

# Paths to model and labels
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'keypoint_classifier', 'model.tflite')
LABEL_PATH = os.path.join(os.path.dirname(__file__), 'keypoint_classifier', 'label.csv')

classifier = KeyPointClassifier(MODEL_PATH)
with open(LABEL_PATH, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Shared variable to store the latest prediction
latest_prediction = ""

def generate_frames():
    global latest_prediction
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        keypoints, _ = detect_hands(frame)

        if keypoints:
            prediction = classifier(keypoints)
            predicted_label = labels[prediction]
            latest_prediction = predicted_label
            cv2.putText(frame, f'Prediction: {predicted_label}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            latest_prediction = ""
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

def get_latest_prediction():
    return latest_prediction
