# SimpleFTCVision

This is a test at using two logictech c922 webcams mounted facing forward on the robot at approximately 18cm apart to localize on yellow powerplay pole. 

In the blender folder there is a blender file that contains a yellow cylinder that serves as the pole and two perspective cameras that serve as the two webcams.
The cameras were given the focal length as measured for the c922 using the code in the camera_calibration folder.  The blender file also contains a blender bpy python
script that moves the pole around to various positions within the FoV of the two cameras and saves off the rendered images of both the left and the right camera.
Finally, the localization_test.py script will use the left and right camera images to estimate the position of the pole from the images.

Run the blender script from within blender.

To run the other scripts you will need to install opencv for python.  I did this within a miniconda (anaconda) environment using python 3.11 with the opencv conda package installed.   
