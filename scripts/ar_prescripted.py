#!/usr/bin/env python2
import rospy

from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Empty

def run_auto():
    takeoff = rospy.Publisher('ardrone/takeoff', Empty)
    land = rospy.Publisher('ardrone/land', Empty)

    cmd_vel = rospy.Publisher('ardrone/cmd_vel', Twist, queue_size=10)

    takeoff.publish(Empty())

    rospy.sleep(1)
    yield

    cmd_vel.publish(Twist(Vector3(1,0,0), Vector3(0,0,0)))

    rospy.sleep(3)
    yield

    cmd_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,1)))

    rospy.sleep(2)
    yield

    cmd_vel.publish(Twist(Vector3(1,0,0), Vector3(0,0,0)))

    rospy.sleep(3)
    yield

    land.publish(Empty())


def main():
    rospy.init_node('ar_prescripted', anonymous=True)

    step = run_auto()
    while not rospy.is_shutdown():
        try:
            next(step)
        except StopIteration:
            break

if __name__ == '__main__':
    main()
