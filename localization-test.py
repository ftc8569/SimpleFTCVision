import numpy as np
import cv2
import matplotlib.pyplot as plt

# for now assume that both left and right cameras have the same intrinsic parameters
# Set the values for the camera matrix
mtx = np.array([[1.01186532e+03, 0.00000000e+00, 8.99900125e+02],
                [0.00000000e+00, 1.01015482e+03, 5.92605177e+02],
                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])


# right now I am using the camera matrix that matches the blender images.  
# the real camera matrix (mtx) was very close for fx but not for cx (blender does not do cx so I think it is basically width/2)
# values below were backsolved for a know location and seem to work well for other locations
fx = 1013.8 # mtx[0,0]
cx = 956.5  # mtx[0,2]

# Load images
source_directory = "./synthetic-images/"
left_image = cv2.imread(source_directory + "depth50cm_y0cm-left.png")
right_image = cv2.imread(source_directory + "depth50cm_y0cm-right.png")
image_height, image_width, _ = left_image.shape

# scale down the images to 320 x 240
# width, height = 320, 240
# left_image = cv2.resize(left_image, (width, height))
# right_image = cv2.resize(right_image, (width, height))

# Convert images to HSV
left_hsv = cv2.cvtColor(left_image, cv2.COLOR_BGR2HSV)
right_hsv = cv2.cvtColor(right_image, cv2.COLOR_BGR2HSV)

# Define range for bright yellow color
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# Create masks to isolate the yellow pole
left_mask = cv2.inRange(left_hsv, lower_yellow, upper_yellow)
right_mask = cv2.inRange(right_hsv, lower_yellow, upper_yellow)

# Collapse images into one dimension by summing along the vertical axis
left_result_sum = np.sum(left_mask, axis=0)
right_result_sum = np.sum(right_mask, axis=0)

# Create convolution kernel and find the maximum of the convolution
kernel_width = image_width // 20
kernel = np.ones(kernel_width)
conv_left = np.convolve(left_result_sum, kernel, mode='valid')
conv_right = np.convolve(right_result_sum, kernel, mode='valid')

# Record the x value of the maximum for each convolution
x_left_conv = np.argmax(conv_left)
x_right_conv = np.argmax(conv_right)

#print the lengths of the convolution and the original array
print("Left convolution length: ", len(conv_left))
print("Left result sum length: ", len(left_result_sum))

# add the kernel width to the x value to get the x value of the maximum in the original array
x_left = x_left_conv + kernel_width // 2
x_right = x_right_conv + kernel_width // 2

# print the peaks
print("Left peak: ", x_left)
print("Right peak: ", x_right)



# plot the images, their filtered versions, and the convolutions using subplots with matplotlib
fig, axs = plt.subplots(4, 2)
axs[0, 0].imshow(left_image)
axs[0, 0].set_title('Left Image')
axs[0, 1].imshow(right_image)
axs[0, 1].set_title('Right Image')
axs[1, 0].imshow(left_mask)
axs[1, 0].set_title('Left Mask')
axs[1, 1].imshow(right_mask)
axs[1, 1].set_title('Right Mask')
axs[2, 0].plot(left_result_sum)
axs[2, 0].set_title('Left Result Sum')
axs[2, 1].plot(right_result_sum)
axs[2, 1].set_title('Right Result Sum')
# Plot a vertial line at the peak of each result sum
axs[2, 0].axvline(x=x_left, color='r', linestyle='--')
axs[2, 1].axvline(x=x_right, color='r', linestyle='--')

# label the result sum peaks with their x values
axs[2, 0].text(x_left, 0, str(x_left))
axs[2, 1].text(x_right, 0, str(x_right))

axs[3, 0].plot(conv_left)
axs[3, 0].set_title('Left Convolution')
axs[3, 1].plot(conv_right)
axs[3, 1].set_title('Right Convolution')

# plot a vertical line at the peak of each convolution
axs[3, 0].axvline(x=x_left_conv, color='r', linestyle='--')
axs[3, 1].axvline(x=x_right_conv, color='r', linestyle='--')

#label the convolution peaks with their x values
axs[3, 0].text(x_left_conv, 0, str(x_left_conv))
axs[3, 1].text(x_right_conv, 0, str(x_right_conv))

fig.tight_layout()
plt.show()

# now use the x values to calculate the distance to the pole
# assume a coordinate system where the origin is directly between the cameras
# the cameras are 18 centimeters apart along the x axis, and the pole is in the positive z direction (in front of the cameras)
# the y axis is the vertical axis, and the x axis is the horizontal axis

left_camera_x = -9 # cm
right_camera_x = 9 # cm

# calculate the slope of the line between the cameras and the pole (this is in pixels/pixel)
# but because the triangle is similar to the real world triangle, the slope is the same in the real world
left_slope = fx /(x_left - cx)
right_slope = fx /(x_right - cx)
print("Left slope: ", left_slope)
print("Right slope: ", right_slope)

# this is basically solving the equation for the intersection of two lines
# the left camera line passing through the point (left_camera_x, 0) with slope left_slope
# the right camera line passing through the point (right_camera_x, 0) with slope right_slope
x_intersection = (left_camera_x * left_slope - right_camera_x * right_slope) / (left_slope - right_slope)
z_intersection = (x_intersection - left_camera_x) * left_slope

# print the intersection point
print("Intersection point: ", x_intersection, z_intersection)

# plot the two lines, the left camera, the right camera and the intersection point, labeled
fig, ax = plt.subplots()
ax.plot([left_camera_x, x_intersection], [0, z_intersection], label='Left Camera Line')
ax.plot([right_camera_x, x_intersection], [0, z_intersection], label='Right Camera Line')
ax.plot([left_camera_x, right_camera_x], [0, 0], label='Camera Line')
ax.plot([left_camera_x], [0], 'o', label='Left Camera')
ax.plot([right_camera_x], [0], 'o', label='Right Camera')
ax.plot([x_intersection], [z_intersection], 'o', label='Intersection')
ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_title('Intersection of Camera Lines')
ax.legend()
plt.show()
