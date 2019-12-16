
from lib.icm import *

from lib.dsply import StuduinoBitDisplay, Image
display = StuduinoBitDisplay()

from time import sleep_ms

compass = StuduinoBitCompass()
print(compass.is_calibrated())
# compass.clear_calibration()
compass.calibrate()

scale = 22.5
index = 0

while True:
    head = compass.heading()
    print(compass.get_values())

    if (head > (180 - scale)) and (head < (180 + scale)):
        index = 0
    elif (head > (225 - scale)) and (head < (225 + scale)):
        index = 7
    elif (head > (270 - scale)) and (head < (270 + scale)):
        index = 6
    elif (head > (315 - scale)) and (head < (315 + scale)):
        index = 5
    elif (head > (360 - scale)) or (head < scale):
        index = 4
    elif (head > (45 - scale)) and (head < (45 + scale)):
        index = 3
    elif (head > (90 - scale)) and (head < (90 + scale)):
        index = 2
    elif (head > (135 - scale)) and (head < (135 + scale)):
        index = 1
    display.show(Image.ALL_ARROWS[index], delay=500)