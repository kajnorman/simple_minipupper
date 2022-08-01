# simple_minipupper
Hints for modifying the python software on the Minipupper/Pupper -robot.


For Pupper:

There is a description of how the software is organized in the original Pupper-documentation here :
https://pupper.readthedocs.io/en/latest/reference/controller.html
 


For MiniPupper

The general setup is the same (except that  the pigpiod is replaced by some other servo-driver-software)  Starting run_robot in a local copy. 

Names of these services and corresponding files
With a fresh minipupper installation the onboard raspberry will start two services when booted.
Service-name 
(As referred from systemctl)	File name 	Purpose
joystick	/home/ubuntu/Robotics/QuadrupedRobot/PupperCommand/joystick.py	This service connects to the controller through Bluetooth. And forwards commands over udp to the actual run_robot.py
robot	/home/ubuntu/Robotics/QuadrupedRobot/StanfordQuadruped/run_robot.py	Controls servoes according to commands received.

 
About the services. (joystick and robot)

Some general info about handling services can be found here : https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units


 
 
Writing(or modifying) your first minipupper program.
First of all you want to stop the installed services to interfere with the program that you will be designing and testing.  Issue the commands 
 
For starters you might base your program on the already existing robot software so you might copy this to your personal created directory.
Create directory and goto directory
 
Copy original file to directory (name it something new)
 
Do your first testrun of your “own” minipupper software.( just to see what happens)
 
The program: warns about some driver versions, reads calibration parameters and creates a joysticklistener and ends by waiting for L1 on the controller. This is all expected.
Issuing a Ctrl-c will stop the program again. 
 
Edit this new program-file using nano.  or use the supplied file!!!
 


