#!/usr/bin/env python2

import os
import random
import rospy
import sys
import threading

import tf
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import Imu

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.tools.customxml import NetworkWriter, NetworkReader

myo_data_lock = threading.Lock()
myo_data = (0.0, 0.0, 0.0)

joystick_lock = threading.Lock()
joystick_data = (0.0, 0.0, 0.0)

def myo_callback(imu):
    global myo_data
    ori = imu.orientation
    x,y,z = tf.transformations.euler_from_quaternion(
        (ori.x, ori.y, ori.z, ori.w))
    with myo_data_lock:
        myo_data = (x, y, z)

def joystick_callback(twist):
    global joystic_data
    l = twist.linear
    with joystick_lock:
        joystick_data = (l.x, l.y, l.z)

def main():
    rospy.init_node('myo_training', anonymous=True)

    #imu_sub = rospy.Subscriber("myo_imu", Imu, myo_callback)
    #joy_sub = rospy.Subscriber("cmd_vel", Twist, joystick_callback)

    if len(sys.argv[1:]) >= 1 and os.path.exists(sys.argv[1]):
        print "Loading from %s" % sys.argv[1]
        net = NetworkReader.readFrom(sys.argv[1])
    else:
        print "Starting new network"
        net = buildNetwork(3, 3)

    #trainSet = SupervisedDataSet(3, 3)

    #rate = rospy.Rate(10)

    #print "Press enter to start collection.",
    #raw_input() 

    #print "Beginning Data Collection"

    #for i in range(1200):
    #    with myo_data_lock, joystick_lock:
    #        trainSet.addSample(myo_data, joystick_data)
    #        print "Added", myo_data, joystick_data
    #    rate.sleep()

    #imu_sub.unregister()
    #joy_sub.unregister()

    #print "Starting Training"

    #trainer = BackpropTrainer(net, trainSet)

    #trainer.trainUntilConvergence()

    #print "Training Completed"

    #if len(sys.argv[1:]) >= 1:
    #    print "Saving trained network in %s" % sys.argv[1]
    #    NetworkWriter.writeToFile(net, sys.argv[1])

    print "Running rest of input on network"

    def run_network(imu):
        ori = imu.orientation
        x,y,z = tf.transformations.euler_from_quaternion(
            (ori.x, ori.y, ori.z, ori.w))
        print net.activate((x,y,z))

    imu_sub = rospy.Subscriber("myo_imu", Imu, run_network)

    rospy.spin()

if __name__ == '__main__':
    main()
