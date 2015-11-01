#!/usr/bin/env python2
from __future__ import print_function

import rospy

import tf
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import Imu

def main():
    rospy.init_node('myo_ar', anonymous=True)

    # Publish to AR drone cmd_vel
    arPub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    # handler for myo_imu subscriber.
    def myo_msg_handle(imu):
        ori = imu.orientation

        print(ori)
        x,y,z = tf.transformations.euler_from_quaternion(
            (ori.x, ori.y, ori.z, ori.w))

        print(x, y, z)

        arPub.publish(Twist(Vector3(x, y, z), Vector3(0,0,0)))

    rospy.Subscriber("myo_imu", Imu, myo_msg_handle)

    rospy.spin()

if __name__ == '__main__':
    main()
