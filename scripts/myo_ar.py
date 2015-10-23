#!/usr/bin/env python2
import rospy

from geometry_msgs.msg import Twist, Vector3
from ros_myo.msg import EmgArray

def main():
    rospy.init_node('myo_ar', anonymous=True)

    # Publish to AR drone cmd_vel
    arPub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    # handler for myo_imu subscriber.
    def myo_msg_handle(emgArr):
        emgArr = emgArr.data

        avgRight = sum(emgArr[0:4]) / 4.0
        avgLeft = sum(emgArr[4:8]) / 4.0
        avgTop = sum(emgArr[2:6]) / 4.0
        avgBottom = sum(emgArr[6:8] + emgArr[0:2]) / 4.0

        move = Vector3(0,0,0)

        if avgLeft > avgRight + 200:
            move.y = 1
        elif avgRight > avgLeft + 200:
            move.y = -1

        if avgTop > avgBottom + 200:
            move.x = -1
        elif avgBottom > avgTop + 200:
            move.x = 1

        print 'Publishing %s' % move

        arPub.publish(Twist(move, Vector3(0,0,0)))

    rospy.Subscriber("myo_emg", EmgArray, myo_msg_handle)

    rospy.spin()

if __name__ == '__main__':
    main()
