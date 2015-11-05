#!/usr/bin/env python2
from __future__ import print_function

import math
import rospy

import tf
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import Imu

def clamp(n, mn, mx):
    return min(max(n, mn), mx)

def main():
    rospy.init_node('myo_ar', anonymous=True)

    # Publish to AR drone cmd_vel
    arPub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    # handler for myo_imu subscriber.
    def myo_msg_handle(imu):
        ori = imu.orientation

        x,y,z = tf.transformations.euler_from_quaternion(
            (ori.x, ori.y, ori.z, ori.w))

        print(x, y, z)

        if abs(y) > math.pi / 4.0:
            f = 1 if y > 0 else -1
        else:
            f = 0

        if abs(z) > math.pi / 5.0:
            h = 1 if z > 0 else -1
        else:
            h = 0
        #f = clamp(y / (math.pi / 4.0), -1.0, 1.0)
        #h = clamp(z / (math.pi / 4.0), -1.0, 1.0)

        arPub.publish(Twist(Vector3(f, h, 0), Vector3(0,0,0)))

    rospy.Subscriber("myo_imu", Imu, myo_msg_handle)

    rospy.spin()

if __name__ == '__main__':
    main()
