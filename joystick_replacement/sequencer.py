import os

from UDPComms import Publisher, Subscriber, timeout

import time

## Configurable ##
MESSAGE_RATE = 20

joystick_pub = Publisher(8830,65530)
joystick_subcriber = Subscriber(8840, timeout=0.01)

cycle_counter = 0


msg = {
    "ly": 0,
    "lx": 0,
    "rx": 0,
    "ry": 0,
    "L2": 0,
    "R2": 0,
    "R1": 0,
    "L1": 0,
    "dpady": 0,
    "dpadx": 0,
    "x": 0,
    "square": 0,
    "circle": 0,
    "triangle": 0,
    "message_rate": MESSAGE_RATE,
}


while True:

    if cycle_counter == 40:
        msg['L1'] = 1
    if cycle_counter == 42:
        msg['L1'] = 0
    if cycle_counter == 80:
        msg['R1'] = 1
    if cycle_counter == 82:
        msg['R1'] = 0
    if cycle_counter == 140:
        msg['ly'] = 0.5
    if cycle_counter == 180:
        msg['rx'] = 0.3
    if cycle_counter == 200:
        msg['rx'] = -0.3
    if cycle_counter == 280:
        msg['L1'] = 1
    if cycle_counter == 282:
        msg['L1'] = 0
    if cycle_counter == 300:
        exit()


    cycle_counter = cycle_counter + 1
    joystick_pub.send(msg)

    time.sleep(1 / MESSAGE_RATE)
