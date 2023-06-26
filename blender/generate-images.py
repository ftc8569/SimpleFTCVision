import bpy
import csv
import random

# Specify the number of new positions for the Pole.
num_positions = 25

# Generate the list of new (x, y) positions for the Pole in centimeters.
new_positions_cm = [(random.randint(10, 100), random.randint(-50, 50)) for _ in range(num_positions)]

# Convert positions to meters.
new_positions_m = [(x/100, y/100) for x, y in new_positions_cm]

# Specify the output directory for the images and CSV file.
output_dir = '../synthetic-images/'

# Get references to the Pole and the cameras.
pole = bpy.data.objects['Pole']
camera_left = bpy.data.objects['Camera-Left']
camera_right = bpy.data.objects['Camera-Right']

# Set up the render settings.
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Open the CSV file for writing.
with open(output_dir + 'positions_and_filenames.csv', 'w', newline='') as csvfile:
    fieldnames = ['x (m)', 'y (m)', 'Camera-Left filename', 'Camera-Right filename']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over the new positions.
    for (x_cm, y_cm), (x_m, y_m) in zip(new_positions_cm, new_positions_m):
        # Move the Pole.
        pole.location.x = x_m
        pole.location.y = y_m

        # Render the image from Camera-Left.
        bpy.context.scene.camera = camera_left
        left_filename = 'Camera-Left_x{}cm_y{}cm.png'.format(x_cm, y_cm)
        bpy.context.scene.render.filepath = output_dir + left_filename
        bpy.ops.render.render(write_still=True)

        # Render the image from Camera-Right.
        bpy.context.scene.camera = camera_right
        right_filename = 'Camera-Right_x{}cm_y{}cm.png'.format(x_cm, y_cm)
        bpy.context.scene.render.filepath = output_dir + right_filename
        bpy.ops.render.render(write_still=True)

        # Write the data to the CSV file.
        writer.writerow({'x (m)': x_m, 'y (m)': y_m, 'Camera-Left filename': left_filename, 'Camera-Right filename': right_filename})
