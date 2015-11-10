#!/usr/bin/env python2
from __future__ import print_function

import math
import rospy

import tf
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import Imu
from ros_myo import EmgArray

rotdat = [0.0, 0.0, 0.0]
emgdat = [0.0] * 8

def clamp(n, mn, mx):
    return min(max(n, mn), mx)

def imu_handler(imu):
    ori = imu.orientation

    x,y,z = tf.transformations.euler_from_quaternion(
        (ori.x, ori.y, ori.z, ori.w))

    rotdata = [x,y,z]

def emg_handler(emg):
    emgdat[:] = emg.data[:]

def emg_data(emg)

def main():
    rospy.init_node('myo_ar', anonymous=True)

    # Publish to AR drone cmd_vel
    arPub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    rospy.Subscriber("myo_imu", Imu, imu_handler)
    
    while True:
        x,y,z = rotdat

        print(x, y, z)

        if abs(y) > math.pi / 6.0:
            f = 1 if y > 0 else -1
        else:
            f = 0

        if abs(z) > math.pi / 6.0:
            h = 1 if z > 0 else -1
        else:
            h = 0

        arPub.publish(Twist(Vector3(f, h, 0), Vector3(0,0,0)))


    rospy.spin()

if __name__ == '__main__':
    main()
