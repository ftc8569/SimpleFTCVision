import cv2
import matplotlib.pyplot as plt

# Open the webcam device.
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Capture frame-by-frame
ret, frame = cap.read()

# Convert the image from BGR color (which OpenCV uses) to RGB color
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Release the webcam after use
cap.release()

# Create a figure and a plot
fig, ax = plt.subplots()

# Display the image
ax.imshow(frame_rgb)

# Function to update the status bar with the hovered coordinates
def format_coord(x, y):
    return f'x={x:.1f}, y={y:.1f}'

# Set the formatter function
ax.format_coord = format_coord

# Show the plot
plt.show()
