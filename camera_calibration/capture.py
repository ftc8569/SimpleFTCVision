import cv2
import os

# The index of the image to be saved
image_index = 1

# Create images directory if not exists
if not os.path.exists('./images'):
    os.makedirs('./images')

# Open the webcam device
cap = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('Webcam Feed', frame)

    # Wait for a key press and get the key code
    key = cv2.waitKey(1)

    # If the spacebar (key code 32) was pressed, save an image
    if key == 32:
        cv2.imwrite(f'./images/image_{image_index}.png', frame)
        image_index += 1
        print(f'Image {image_index - 1} saved!')

    # If any key other than the spacebar was pressed, exit the loop
    elif key >= 0:
        break

# Release the webcam and destroy all windows when done
cap.release()
cv2.destroyAllWindows()
