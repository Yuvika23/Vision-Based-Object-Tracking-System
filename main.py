# -----------------------------------------------------
# Project: RoboEye - Vision Based Object Tracking Robot
# Description:
# Detects multiple colored objects in real-time using HSV,
# simulates movement commands + displays color name,
# and provides navigation instructions to reach a random target.
# -----------------------------------------------------

import cv2
import numpy as np
import random
import time

# STEP 1: INPUT (Webcam Feed)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

# STEP 2: COLOR RANGES (HSV)
colors = {
    "Red":   [(np.array([0, 120, 70]), np.array([10, 255, 255])),
              (np.array([170, 120, 70]), np.array([180, 255, 255]))],
    "Blue":  [(np.array([94, 80, 2]), np.array([126, 255, 255]))],
    "Green": [(np.array([35, 100, 100]), np.array([85, 255, 255]))],
    "Yellow":[(np.array([20, 100, 100]), np.array([30, 255, 255]))]
}

# Helper: create a new random target inside frame bounds
def new_random_target(w, h, margin=50):
    tx = random.randint(margin, w - margin)
    ty = random.randint(margin, h - margin)
    return (tx, ty)

# Initialize target after getting a frame size
initialized = False
target = None
target_radius = 12            # how big target pointer looks
reach_threshold = 30         # pixels within which object is considered to have reached the target

# A small cool-down after reaching target to show message before new target
target_reached_time = 0
target_reached_cooldown = 0.8  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not accessible!")
        break

    # Initialize target once we know frame size
    if not initialized:
        frame = cv2.flip(frame, 1)
        frame_height, frame_width = frame.shape[:2]
        target = new_random_target(frame_width, frame_height)
        initialized = True

    frame = cv2.flip(frame, 1)  # mirror
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    direction = "No Object Detected"
    detected_color = None
    nav_instruction = ""  # instruction to reach target
    cx = cy = None

    for color_name, ranges in colors.items():
        mask = None

        # Build mask for this color (supports multi-range like red)
        for (lower, upper) in ranges:
            part_mask = cv2.inRange(hsv, lower, upper)
            mask = part_mask if mask is None else cv2.bitwise_or(mask, part_mask)

        # Clean mask
        mask = cv2.GaussianBlur(mask, (7, 7), 0)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=1)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(contour)

            if area > 800:
                x, y, w, h = cv2.boundingRect(contour)
                cx = x + w // 2
                cy = y + h // 2

                frame_height, frame_width, _ = frame.shape

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.circle(frame, (cx, cy), 7, (255, 0, 0), -1)
                cv2.line(frame, (cx, 0), (cx, frame_height), (255, 0, 0), 2)

                # Direction logic (basic left/center/right used for legacy display)
                if cx < frame_width / 3:
                    direction = "Move Left"
                elif cx > 2 * frame_width / 3:
                    direction = "Move Right"
                else:
                    direction = "Move Forward"

                detected_color = color_name
                break  # Stop after detecting one major color

        if detected_color:
            break

    # ====== Navigation to Target Logic ======
    if target is None:
        target = new_random_target(frame_width, frame_height)

    tx, ty = target

    # Draw the target using a black pointer (filled circle)
    # Use a white border so the black circle is visible on dark backgrounds
    cv2.circle(frame, (tx, ty), target_radius + 4, (255, 255, 255), -1)  # white border
    cv2.circle(frame, (tx, ty), target_radius, (0, 0, 0), -1)            # black pointer (center)

    if cx is not None and cy is not None:
        dx = tx - cx
        dy = ty - cy
        dist = int(np.hypot(dx, dy))

        # Horizontal instruction
        horiz = ""
        if abs(dx) > reach_threshold:
            horiz = "Move Right" if dx > 0 else "Move Left"

        # Vertical instruction
        vert = ""
        if abs(dy) > reach_threshold:
            vert = "Move Down" if dy > 0 else "Move Up"

        # Combine instructions
        if horiz and vert:
            nav_instruction = f"{horiz} & {vert}"
        elif horiz:
            nav_instruction = horiz
        elif vert:
            nav_instruction = vert
        else:
            nav_instruction = "Target Reached"

            # Register reach timestamp and create a new target after cooldown
            if time.time() - target_reached_time > target_reached_cooldown:
                target_reached_time = time.time()
                # small pause to show the reach message before moving target
                # set next target after a short delay
                target = new_random_target(frame_width, frame_height)

        # draw a line from object center to target for visual guidance
        cv2.line(frame, (cx, cy), (tx, ty), (200, 200, 200), 2)
        # show distance
        cv2.putText(frame, f"Dist: {dist}px", (40, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    else:
        nav_instruction = "No object to navigate"

    # STEP 6: DISPLAY INFO
    if detected_color:
        cv2.putText(frame, f"Detected: {detected_color}",
                    (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

    cv2.putText(frame, f"Direction: {direction}",
                (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Show navigation instruction prominently
    cv2.putText(frame, f"Navigate: {nav_instruction}",
                (40, frame_height - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 165, 255), 3)

    cv2.imshow("RoboEye - Multi-Color Tracking with Target", frame)

    # Only ONE exit condition — press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
