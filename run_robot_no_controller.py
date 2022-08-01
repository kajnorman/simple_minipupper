import os
import sys
import threading
import time

import numpy as np
from PIL import Image
from multiprocessing import Process
import multiprocessing

sys.path.append("/home/ubuntu/Robotics/QuadrupedRobot")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("/home/ubuntu/Robotics/QuadrupedRobot") for name in dirs])
from Mangdang.LCD.ST7789 import ST7789
from Mangdang.LCD.gif import AnimatedGif
from src.Controller import Controller
from src.State import State
from pupper.MovementGroup import MovementLib
from src.MovementScheme import MovementScheme
from pupper.HardwareInterface import HardwareInterface
from pupper.Config import Configuration
from pupper.Kinematics import four_legs_inverse_kinematics
from Command import Command  #new

quat_orientation = np.array([1, 0, 0, 0])

cartoons_folder = "/home/ubuntu/Robotics/QuadrupedRobot/Mangdang/LCD/cartoons/"
current_show = ""
disp = ST7789()
command = Command()  #no initializer ??

def pic_show(disp, pic_name, _lock):
    """ Show the specify picture
        Parameter:
            disp : display instance
            pic_name : picture name to show
        Return : None
    """
    if pic_name == "":
        return

    global current_show
    if pic_name == current_show:
        return

    image=Image.open(cartoons_folder + pic_name)
    image.resize((320,240))
    _lock.acquire()
    disp.display(image)
    _lock.release()
    current_show = pic_name

def animated_thr_fun(_disp, duration, is_connect, current_leg, _lock):
    """
    The thread funcation to show sleep animated gif
    Parameter: None
    Returen: None
    """
    try:
        gif_player = AnimatedGif(_disp, width=320, height=240, folder=cartoons_folder)
        last_time = time.time()
        last_joint_angles = np.zeros(3)
        while True:
            if is_connect.value == 1 :
                #if ((current_leg[0]==last_joint_angles[0]) and  (current_leg[1]==last_joint_angles[1]) and (current_leg[2]==last_joint_angles[2])) == False :
                if ((current_leg[0]==last_joint_angles[0]) and  (current_leg[1]==last_joint_angles[1])) == False :
                    last_time = time.time()
                    last_joint_angles[0] = current_leg[0]
                    last_joint_angles[1] = current_leg[1]
                    #last_joint_angles[2] = current_leg[2]
                if (time.time() - last_time) > duration :
                    _lock.acquire()
                    gif_player.play()
                    _lock.release()
                    time.sleep(0.5)
            else :
                 last_time = time.time()
                 time.sleep(1.5)
    except KeyboardInterrupt:
        _lock.release()
        pass


def main():
    """Main program
    """
    # Create config
    config = Configuration()
    hardware_interface = HardwareInterface()

    # show logo
    global disp
    disp.begin()
    disp.clear()
    image=Image.open(cartoons_folder + "logo.png")
    image.resize((320,240))
    disp.display(image)

    shutdown_counter = 0            # counter for shuudown cmd

    # Start animated process
    duration = 10
    is_connect = multiprocessing.Value('l', 0)
    current_leg = multiprocessing.Array('d', [0, 0, 0])
    lock = multiprocessing.Lock()
    animated_process = Process(target=animated_thr_fun, args=(disp, duration, is_connect, current_leg, lock))
    #animated_process.start()

    #Create movement group scheme
    movement_ctl = MovementScheme(MovementLib)

    # Create controller and user input handles
    controller = Controller(
        config,
        four_legs_inverse_kinematics,
    )
    state = State()

    last_loop = time.time()

    print("Summary of gait parameters:")
    print("overlap time: ", config.overlap_time)
    print("swing time: ", config.swing_time)
    print("z clearance: ", config.z_clearance)
    print("x shift: ", config.x_shift)

    while True:
        is_connect.value = 1
        pic_show(disp, "walk.png", lock)
        start_time = time.time()

        while True:
            now = time.time()
            if now - last_loop < config.dt:
                continue
            last_loop = time.time()
            _pic = "walk.png" if command.yaw_rate ==0 else "turnaround.png"
            if command.trot_event == True:
                _pic = "walk_r1.png"
            pic_show(disp, _pic, lock)
            if command.activate_event == 1:  #if L1 is pressed again the   robot is deactivated...
                is_connect.value = 0
                pic_show(disp, "notconnect.png", lock)
                print("Deactivating Robot")
                break
            state.quat_orientation = quat_orientation
            # movement scheme
            movement_switch = command.dance_switch_event
            gait_state = command.trot_event
            dance_state = command.dance_activate_event
            shutdown_signal = command.shutdown_signal


            # gait and movement control
            if gait_state == True or dance_state == True:       # if triger tort event, reset the movement number to 0
                movement_ctl.resetMovementNumber()
            movement_ctl.runMovementScheme(movement_switch)
            food_location = movement_ctl.getMovemenLegsLocation()
            attitude_location = movement_ctl.getMovemenAttitudeLocation()
            controller.run(state,command,food_location,attitude_location)

            # Update the pwm widths going to the servos
            hardware_interface.set_actuator_postions(state.joint_angles)
            current_leg[0]= state.joint_angles[0][0]
            current_leg[1]= state.joint_angles[1][0]
            #current_leg[2]= state.joint_angles[2][0]

            #START  of the SEQENCER ##################
            if start_time + 0 < now < start_time + 2:
                print("command.trot_event = 0");
                command.trot_event = 0;
            if start_time + 2 < now < start_time + 2 + config.dt:
                print("command.trot_event = 1");
                command.trot_event = 1;
            if start_time + 2+ config.dt < now < start_time + 4 :
                print("command.trot_event = 0");
                command.trot_event = 0;
            if start_time + 6 < now < start_time + 6 + config.dt:
                print("command.trot_event = 1");
                command.trot_event = 1;
            if start_time + 6 + config.dt < now:
                print("command.trot_event = 0");
                command.trot_event = 0;
            if start_time + 10 < now:
                exit();


try:
    main()
except KeyboardInterrupt:
    pass