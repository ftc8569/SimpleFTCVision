import math
import numpy as np

# Calculate field of view
width = 1920
height = 1080

# Set the values for the camera matrix
mtx = np.array([[1.01186532e+03, 0.00000000e+00, 8.99900125e+02],
                [0.00000000e+00, 1.01015482e+03, 5.92605177e+02],
                [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])



# Camera matrix values
fx = mtx[0,0]
fy = mtx[1,1]

# Calculate field of view
fov_horizontal = 2 * math.atan(width / (2*fx))
fov_vertical = 2 * math.atan(height / (2*fy))

# Convert from radians to degrees
fov_horizontal = math.degrees(fov_horizontal)
fov_vertical = math.degrees(fov_vertical)

print("Horizontal Field of View : ", fov_horizontal)
print("Vertical Field of View : ", fov_vertical)