# ml_model/hand_detection.py

import cv2
import numpy as np
import mediapipe as mp

# Initialize mediapipe modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Function to detect hands and extract keypoints

from ml_model.hand_utils import calc_landmark_list, pre_process_landmark

def detect_hands(image):
    with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]

            # Apply preprocessing
            landmark_point = calc_landmark_list(image, landmarks)
            keypoints = pre_process_landmark(landmark_point)

            return keypoints, landmarks
        else:
            return None, None
