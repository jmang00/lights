import yaml
from models.camera import CameraGroup
from models.leds import LEDArray

# Load settings
with open('settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Setup LEDs
print('Initializing LEDs...')
leds = LEDArray(config)

# Setup local camera(s)
print('Initializing cameras...')
cams = CameraGroup(config)  

# Import positions
# positions = np.genfromtxt('/home/pi/lights/scans/{scan_name}/positions.csv', delimiter=',')

# # Iterate over each column and fill NaN values with the last non-NaN value
# for col in range(positions.shape[1]):
#     non_nan_indices = np.where(~np.isnan(positions[:, col]))[0]
#     last_non_nan_index = non_nan_indices[-1] if non_nan_indices.size > 0 else 0
#     positions[:, col][np.isnan(positions[:, col])] = positions[last_non_nan_index, col]

if __name__ == '__main__':
    print('Running basic test effect...')
    
    while True:
        leds.set_all_white()
        leds.basic_cycle()
    
    # # Random green/red cycling
    # while True:
    #     for i in range(NO_LEDS):
    #         r = random.randint(1,2)

    #         if r == 1:
    #             leds[i] = (255, 0, 0)
    #         else:
    #             leds[i] = (0, 255, 0)

    #     leds.show()
    #     time.sleep(2)
    

    # Turn on in batches
    # batch = 10
    # for i in range(50):
    #     leds[i*batch:(i+1)*batch] = (255, 0, 0)
    #     leds.show()
    #     time.sleep(1)
    #     leds[i*batch:(i+1)*batch] = (0, 0, 0)