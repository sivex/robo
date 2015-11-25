#!/usr/bin/env python2
from __future__ import print_function

import enum
import math
import rospy
import threading

import tf
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import Imu
from std_msgs.msg import UInt8, Empty

class Pose(enum.Enum):
    REST = 0
    FIST = 1
    WAVE_IN = 2
    WAVE_OUT = 3
    FINGERS_SPREAD = 4
    THUMB_TO_PINKY = 5
    UNKNOWN = 255

rotlock = threading.Lock()
rotdat = [0.0, 0.0, 0.0]

rotlock2 = threading.Lock()
rotdat2 = [0.0, 0.0, 0.0]

def clamp(n, mn, mx):
    return min(max(n, mn), mx)

def imu_handler(imu):
    global rotdat

    #print('IMU HANDLER')

    ori = imu.orientation

    x,y,z = tf.transformations.euler_from_quaternion(
        (ori.x, ori.y, ori.z, ori.w))

    #print(x, y, z)

    with rotlock:
        rotdat = [x,y,z]

def imu_handler2(imu):
    global rotdat2

    #print('IMU HANDLER')

    ori = imu.orientation

    x,y,z = tf.transformations.euler_from_quaternion(
        (ori.x, ori.y, ori.z, ori.w))

    #print(x, y, z)

    with rotlock2:
        rotdat2 = [x,y,z]


def main():
    rospy.init_node('myo_ar', anonymous=True)

    # Publish to AR drone cmd_vel
    arPub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    takeoff = rospy.Publisher('ardrone/takeoff', Empty, queue_size=1) 
    land = rospy.Publisher('ardrone/land', Empty, queue_size=1) 
    reset = rospy.Publisher('ardrone/reset', Empty, queue_size=1)

    def gest_handler(msg):
        #print('GEST HANDLER')
        data = Pose(msg.data)
        print(data)
        if data == Pose.FINGERS_SPREAD:
            takeoff.publish(Empty())
            print('Takeoff')
        elif data == Pose.FIST:
            land.publish(Empty())
            print('Land')
        #elif data == Pose.:
        #    reset.publish(Empty())
        #    print('Reset')

    rospy.Subscriber('myo_imu1', Imu, imu_handler)
    rospy.Subscriber('myo_imu2', Imu, imu_handler2)
    rospy.Subscriber('myo_gest1', UInt8, gest_handler)

    rate = rospy.Rate(60)
    
    while True:
        with rotlock:
            x,y,z = rotdat

        if abs(y) > math.pi / 6.0:
            f = 1 if y > 0 else -1
        else:
            f = 0

        if abs(z) > math.pi / 6.0:
            h = 1 if z > 0 else -1
        else:
            h = 0

        with rotlock2:
            x,y,z = rotdat2

        if abs(y) > math.pi / 6.0:
            v = -1 if y > 0 else 1
        else:
            v = 0

        if abs(z) > math.pi / 6.0:
            r = 1 if z > 0 else -1
        else:
            r = 0

        #print(f, h)

        arPub.publish(Twist(Vector3(f, h, v), Vector3(0,0,r)))

        rate.sleep()


if __name__ == '__main__':
    main()
