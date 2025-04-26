import sys
import os

# Add the parent directory of 'ml_model' to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import numpy as np
from ml_model.hand_detection import detect_hands
from ml_model.keypoint_classifier import KeyPointClassifier

# Define the absolute path to the model and labels
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'keypoint_classifier', 'model.tflite')
LABEL_PATH = os.path.join(os.path.dirname(__file__), 'keypoint_classifier', 'label.csv')

# Load classifier and labels
classifier = KeyPointClassifier(MODEL_PATH)  # This uses the correct path to load your model
with open(LABEL_PATH, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Function to start webcam and predict signs
def start_video():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip image for natural mirror view
        frame = cv2.flip(frame, 1)

        # Detect hand & extract keypoints
        keypoints, landmarks = detect_hands(frame)

        if keypoints:
            # Predict label using classifier
            prediction = classifier(keypoints)

            

            predicted_label = labels[prediction]

            # Display prediction
            cv2.putText(frame, f'Prediction: {predicted_label}', (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            predicted_label = ""

        # Show the webcam feed with prediction
        cv2.imshow("Hand Sign Recognition", frame)

        # Break loop on pressing 'q' or 'esc'
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Start video feed
start_video()
