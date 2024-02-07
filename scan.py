# Scans the lights, and saves the image scans to a folder.
import yaml
import os
from datetime import datetime
import time
from models.camera import CameraGroup
from models.leds import LEDArray
from models.scan import Scan

# Load settings
with open('settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

print('Loaded settings from setting.yaml. Edit that file and rerun to change settings.')


# Check if scan already exists
scan_name = config['SCAN_NAME']

if os.path.isdir(f'scans/{scan_name}'):
    input('Scan already exists. Press Enter to overwrite, or Ctrl+C to cancel')

else:
    os.mkdir(f'scans/{scan_name}')
    os.mkdir(f'scans/{scan_name}/images')


# Setup LEDs
print('Initializing LEDs...')
leds = LEDArray(config)

# Setup local camera(s)
print('Initializing cameras...')
cams = CameraGroup(config)
cams.test_all()

start_time = datetime.now()

input('Press Enter to start')

try:
    print('\n~~ Make the room dark ~~')
    input('Press Enter to start the scan')

    x = None
    while x != '':
        # Take a base image from each camera
        for cam in cams:
            cam.save_photo(f'scans/{scan_name}/images/{cam.id}_base.jpg')

        # base_img = cam.take_photo()
        # cv2.imshow('Base Image', base_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # base_img.save(f'{scan_name}/{cam.id}_base.jpg')

        # Check base image
        print('\n~~ Confirm the base images look okay ~~')
        x = input('Press Enter to accept, or enter anything else to take again')

    # Turn on each light one by one, take a photo
    for i in range(len(leds)):
        print(f'Scanning LED {i}')
        
        # Turn on white
        leds[i] = (255, 255, 255)
        leds.show()
        time.sleep(0.1)

        # Read camera
        for cam in cams:
            cam.save_photo(f'scans/{scan_name}/images/{cam.id}_{i}.jpg')

        # Turn off
        leds[i] = (0, 0, 0)
        leds.show()

    # Could have multiple angles/rotation
    # input('Rotate the tree to the next angle, make the room bright again, then press enter to continue')

except Exception as e:
    print(e)

    # Release cam
    cam.release()

# Release camera
cam.release()

end_time = datetime.now()
duration = end_time - start_time


# Save scan details to a yaml file
scan_details = config
scan_details['START_TIME'] = start_time
scan_details['END_TIME'] = end_time
scan_details['DURATION'] = duration

with open(f'scans/{scan_name}/details.yaml', 'w') as f:
    yaml.dump(scan_details, f)


# Process scanned images
print('Processing scanned images...')
scan = Scan(scan_name)
scan.generate_camera_frame_positions()


print('Done!')