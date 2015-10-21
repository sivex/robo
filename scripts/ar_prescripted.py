#!/usr/bin/env python2
import rospy

from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Empty

PUB_RATE = 50

def forward(time, cmd_vel):
    """Move forward for time seconds"""
    rate = rospy.Rate(PUB_RATE)
    end = rospy.get_time() + time

    while rospy.get_time() < end:
        cmd_vel.publish(Twist(Vector3(1,0,0), Vector3(0,0,0)))
        rate.sleep()
        yield

def turn(time, dir, cmd_vel):
    """Turn in dir (+/- 1) for time seconds"""
    rate = rospy.Rate(PUB_RATE)
    end = rospy.get_time() + time
    
    while rospy.get_time() < end:
        cmd_vel.publish(Twist(Vector3(0,0,0), Vector3(0,0,dir)))
        rate.sleep()
        yield

def run_auto(takeoff, land, cmd_vel):
    rospy.sleep(2)

    takeoff.publish(Empty())
    print 'Takeoff'

    rospy.sleep(2)
    yield

    for i in forward(3, cmd_vel): pass

    for i in turn(1, 1, cmd_vel): pass

    for i in forward(3, cmd_vel): pass
    
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
