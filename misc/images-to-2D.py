# Analyse the images to find the position of each LED in for angle frame

# Input: a folder of images
# Output: a positions_camera_frame.npy file

import numpy as np
import cv2

NO_LEDS = 300
scan_name = 'torquay-flat'

angles = [
    0
]

def find_brightest_pixel(image):
    width, height = image.shape[:2]
    brightest_pixel = (0, 0)
    max_brightness = 0

    for x in range(width):
        for y in range(height):
            pixel = [y,x]
            # Calculate the brightness of the pixel (you can use different formulas)
            brightness = sum(pixel)  # Sum of R, G, and B values

            if brightness > max_brightness:
                max_brightness = brightness
                brightest_pixel = (x, y)

    return brightest_pixel


def find_circular_light_pixels(image, intensity_threshold, min_radius, max_radius, avoid_left_region, debug=False):
    # Input:
    # image
    # intensity_threshold
    # min_radius
    # max_radius
    # avoid_left_region
    
    # Convert image to a cv2 image
    image = np.array(image)
    # # Convert RGB to BGR
    # open_cv_image = open_cv_image[:, :, ::-1].copy()

    # Check if the image is successfully loaded
    if image is not None:
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
        # Apply Gaussian blur
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
 
        # Apply intensity thresholding to the blurred image
        _, binary_image = cv2.threshold(blurred_image, intensity_threshold, 255, cv2.THRESH_BINARY)
 
        # Apply Hough Circle Transform
        circles = cv2.HoughCircles(
            binary_image, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
            param1=40, param2=5, minRadius=min_radius, maxRadius=max_radius
        )
 
        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            # Filter circles based on the left region to avoid
            filtered_circles = [circle[0:2] for circle in circles[0, :] if circle[0] > avoid_left_region]
 
            if filtered_circles:
                pixel_coordinates = [tuple(coord) for coord in filtered_circles]

                if debug:
                    # Visualize the circles on the original image
                    for i in circles[0, :]:
                        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
    
                    # Display the image with circles
                    cv2.imshow('Circle', image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                return pixel_coordinates
            else:
                print("No circular light sources found in the specified region.")
                return None
        else:
            print("No circular light sources found.")
            return None

# Open base images
base_img = {}
for angle in angles:
    base_img[angle] = cv2.imread(f'{scan_name}/0_{angle}_base.jpg')


# Setup positions array
# positions_camera_frame[angle, led, x/y/z]
positions_camera_frame = np.zeros((4, NO_LEDS, 2))

for i in range(NO_LEDS):
    for angle in angles:
        # Find location of LED in image
        img = cv2.imread(f'{scan_name}/0_{angle}_{i}.jpg')
        base_img = cv2.imread(f'{scan_name}/0_{angle}_base.jpg')


        # print(img)
        # print(base_img)

        # print(img.shape)
        # print(base_img.shape)

        diff_img = cv2.subtract(img, base_img)
        # cv2.imshow('Difference Image', diff_img)

        # # Using the brightest pixel
        # x, y = find_brightest_pixel(  diff_img)

        # Using the circular light source
        intensity_threshold = 130  # Adjust this value based on your images
        shitter_intensity_threshold = 70  # Adjust this value based on your images
        min_radius = 5  # Adjust as needed based on the expected size of the circular light sources
        max_radius = 25  # Adjust as needed based on the expected size of the circular light sources
        avoid_left_region = 150  # Specify the x-coordinate to avoid circles on the left side
        
        coordinates = find_circular_light_pixels(diff_img, intensity_threshold, min_radius, max_radius, avoid_left_region)


        # Show coordinate
        # # Display the image with circles
        # cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)  
        # cv2.imshow('Circles', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        if coordinates is None:
            print(f'LED {i} at angle {angle} not found, repeat with a lower threshhold')
            coordinates = find_circular_light_pixels(diff_img, shitter_intensity_threshold, min_radius, max_radius, avoid_left_region)

        # Save position
        if coordinates is not None:
            positions_camera_frame[angles.index(angle), i] = coordinates[0]

    # TODO - check how many angles worked and redo

# Print info
no_cameras = [
    np.count_nonzero(positions_camera_frame[:,i,:])/2
    for i in range(NO_LEDS)
]

freq_no_cameras = np.unique(no_cameras, return_counts=True)
freq_no_cameras = np.array(freq_no_cameras).T
print(freq_no_cameras)

# Save as a numpy object (for the next python script)
np.save(f'{scan_name}/positions_camera_frame.npy', positions_camera_frame)

# Split into 4 csvs and save (so Mathematica can read them)
for angle in angles:
    np.savetxt(
        f'{scan_name}/positions_camera_frame_{angle}.csv',
        positions_camera_frame[angles.index(angle)],
        delimiter=','
    )