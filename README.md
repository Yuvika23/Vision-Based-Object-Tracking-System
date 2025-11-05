# 🤖 RoboEye – Vision-Based Object Tracking Robot

### 🧠 Author: **Yuvika Gandhi**

RoboEye is a **computer vision–based virtual robot** that detects and tracks colored objects in real time using a webcam.  
It simulates **intelligent robotic movement** by identifying object positions, recognizing colors, and giving navigation instructions such as **“Move Left,” “Move Right,” “Move Up,”** or **“Move Forward.”**  

---

## 🚀 Project Overview

RoboEye is designed to demonstrate how **computer vision** can enable autonomous robots to make movement decisions based purely on visual input.  
It uses **OpenCV** and **NumPy** to process live video frames, detect specific colors using the **HSV color space**, and visualize object tracking along with direction guidance.

In the extended version, RoboEye includes a **target navigation feature** — where a random target point appears on the screen, and the robot (detected object) receives instructions to move toward it.  
This mimics the behavior of **real-world autonomous robots** that navigate toward goals based on visual feedback.

---

## ⚙️ Technologies Used

- **Python 3**
- **OpenCV** (Computer Vision & Image Processing)
- **NumPy** (Matrix Operations)
- **HSV Color Detection**
- **Contour Detection and Object Tracking**
- **Target-Based Navigation Simulation**

---

## 🧩 Features

✅ Detects multiple colors (Red, Blue, Green, Yellow) in real time  
✅ Recognizes and displays color name on screen  
✅ Highlights object with bounding box and center marker  
✅ Displays **direction commands** (“Move Left,” “Move Right,” “Move Forward”)  
✅ Generates a random **target point** and provides navigation guidance toward it  
✅ Works purely on **software simulation** — no external hardware required  

---

## 🧠 Working Principle

1. **Input (Webcam Feed):**  
   Captures real-time video from the webcam.

2. **Image Processing:**  
   Converts each frame from BGR to HSV color space for easier color detection.

3. **Color Detection & Masking:**  
   Applies HSV range filters to detect specific colors. Uses contour extraction to locate the colored object.

4. **Position Analysis:**  
   Calculates the center coordinates of the detected object.

5. **Decision Logic:**  
   Compares object position with the screen’s center or a target point and prints movement directions.

6. **Output Display:**  
   Displays bounding boxes, color names, and directional instructions directly on the video feed.
