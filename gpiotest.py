import sys
import os
import time


sys.path.append("/home/ubuntu/Robotics/QuadrupedRobot")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("/home/ubuntu/Robotics/QuadrupedRobot") for name in dirs])
import GPIO as GPIO



gpio =  GPIO.get_platform_gpio()


gpio.setup(19,0)  # 0 for out

while True:
   gpio.set_high(19)
   time.sleep(1)
   gpio.set_low(19)
   time.sleep(1)



