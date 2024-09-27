import cv2
import serial
import time

# Initialize serial connection to Arduino
arduino = serial.Serial('COM3', 9600)  # Change 'COM3' to your Arduino port
time.sleep(2)

# Load pre-trained Haar Cascade model for human detection
human_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# Start video capture (use 0 for webcam or video path) 
cap = cv2.VideoCapture(0)

while True:
    # Read each frame from the video source
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    
    # Detect humans in the frame
    humans = human_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

    
    if len(humans) > 0:
        print("Person detected")
        arduino.write(b'1')  # Send signal to Arduino to turn on LED
    else:
        arduino.write(b'0')  # Send signal to turn off LED

    # Draw rectangles around detected humans
    for (x, y, w, h) in humans:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Show the video feed
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
arduino.close()