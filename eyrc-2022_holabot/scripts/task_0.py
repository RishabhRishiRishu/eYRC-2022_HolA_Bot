#!/usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		    HolA Bot (HB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script should be used to implement Task 0 of HolA Bot (KB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ hb_2563 ]
# Author List:		[ Rishabh, Arvind, Jordan, Mukul ]
# Filename:			task_0.py
# Functions:        [ callback, main ]
# Nodes:		    [ /turtle1/cmd_vel, /turtle1/pose]


####################### IMPORT MODULES #######################
import sys
import traceback
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
##############################################################


def callback(data:Pose):
    """
    Purpose:
    ---
    This function should be used as a callback. Refer Example #1: Pub-Sub with Custom Message in the Learning Resources Section of the Learning Resources.
    You can write your logic here.
    NOTE: Radius value should be 1. Refer expected output in document and make sure that the turtle traces "same" path.

    Input Arguments:
    ---
        `data`  : []
            data received by the call back function

    Returns:
    ---
        May vary depending on your logic.

    Example call:
    ---
        Depends on the usage of the function.
    """
    global STAGE, START_POINT, VEL_MSG
    if STAGE==-1: # first callback
        STAGE = 0
        START_POINT = (data.x, data.y) # saves start point
    elif STAGE==0 and data.theta>3.13: # Reached end point of arc
        STAGE = 1
    elif STAGE==1 and data.theta>=(-1.57): # Made the turn towards start
        STAGE = 2
    elif STAGE==2 and data.y<START_POINT[1]: # Crossed the initial point
        STAGE = 3
        print('Done!!')

    # change speeds
    if STAGE==-1:
        pass
    elif STAGE==0:
        VEL_MSG.linear.x = 1
        VEL_MSG.angular.z = 1
        print('My turtleBot is: Moving in circle!!')
    elif STAGE==1:
        VEL_MSG.linear.x = 0
        VEL_MSG.angular.z = 1
        print('My turtleBot is: Rotating!')
    elif STAGE==2:
        VEL_MSG.linear.x = 1
        VEL_MSG.angular.z = 0
        print('My turtleBot is: Moving Straight!!!')
    elif STAGE==3:
        VEL_MSG.linear.x = 0
        VEL_MSG.angular.z = 0
        velocity_publisher.publish(VEL_MSG)
        STAGE=4
    velocity_publisher.publish(VEL_MSG)
    if STAGE<4:
        print(f"{data.theta:.2f}")
    return(1)


def main():
    """
    Purpose:
    ---
    This function will be called by the default main function given below.
    You can write your logic here.

    Input Arguments:
    ---
        None

    Returns:
    ---
        None

    Example call:
    ---
        main()
    """
    global STAGE, velocity_publisher, VEL_MSG

    # setup Publisher and subscriber
    rospy.init_node('turtle_revolve', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber("/turtle1/pose", Pose, callback)
    rate = rospy.Rate(1000)


    # make twist object
    VEL_MSG = Twist()
    VEL_MSG.angular.x = 0
    VEL_MSG.angular.y = 0
    VEL_MSG.angular.z = 0
    VEL_MSG.linear.x = 0
    VEL_MSG.linear.y = 0
    VEL_MSG.linear.z = 0
    

    # main logic
    STAGE = -1
    while not rospy.is_shutdown():
        if STAGE==4:
            break
        rate.sleep()


################# ADD GLOBAL VARIABLES HERE #################
STAGE = -1
PI = 3.14159
START_POINT = None
VEL_MSG = None
velocity_publisher = None
# PREV_DATA = 0

##############################################################


################# ADD UTILITY FUNCTIONS HERE #################



##############################################################


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS PART #########
if __name__ == "__main__":
    try:
        print("------------------------------------------")
        print("         Python Script Started!!          ")
        print("------------------------------------------")
        main()

    except:
        print("------------------------------------------")
        traceback.print_exc(file=sys.stdout)
        print("------------------------------------------")
        sys.exit()

    finally:
        print("------------------------------------------")
        print("    Python Script Executed Successfully   ")
        print("------------------------------------------")
