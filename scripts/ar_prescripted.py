#!/usr/bin/env python2
import rospy

from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Empty

PUB_RATE = 50

def run_auto(takeoff, land, cmd_vel):
    rospy.sleep(2)

    takeoff.publish(Empty())
    print 'Takeoff'

    rospy.sleep(2)
    yield

    cmd_vel.publish(Twist(Vector3(1,0,0), Vector3(0,0,0)))
    rospy.sleep(3)
    yield

    cmd_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,1)))
    rospy.sleep(1.5)
    yield

    cmd_vel.publish(Twist(Vector3(1,0,0), Vector3(0,0,0)))
    rospy.sleep(3)
    yield

    cmd_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,0)))
    rospy.sleep(1)
    yield

    land.publish(Empty())
    print 'Land'


def main():
    takeoff = rospy.Publisher('ardrone/takeoff', Empty, queue_size=1)
    land = rospy.Publisher('ardrone/land', Empty, queue_size=1)
    cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    rospy.init_node('ar_prescripted', anonymous=True)

    step = run_auto(takeoff, land, cmd_vel)
    while not rospy.is_shutdown():
        try:
            next(step)
        except StopIteration:
            break

if __name__ == '__main__':
    main()
