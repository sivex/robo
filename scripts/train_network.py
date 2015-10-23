#!/usr/bin/env python2

import random
import rospy
import threading

from ros_myo.msg import EmgArray

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork

myo_data_lock = threading.Lock()
myo_data = [0.0] * 9

def myo_callback(emgArr):
    with myo_data_lock:
        myo_data[:] = emgArr.data[:]

def main():
    rospy.init_node('myo_training', anonymous=True)

    emg_sub = rospy.Subscriber("myo_emg", EmgArray, myo_callback)

    cases = [
        ("Left", [0, -1]),
        ("Right", [0, 1]),
        ("Forward", [1, 0]),
        ("Backward", [-1, 0]),
        ("Forward-Left", [1, -1]),
        ("Forward-Right", [1, 1]),
        ("Backward-Left", [-1, -1]),
        ("Backward-Right", [-1, 1]),
    ]

    net = buildNetwork(9, 12, 2)

    trainSet = SupervisedDataSet(9, 2)

    rospy.sleep(5)

    print "Beginning Data Collection"

    rospy.sleep(2)

    for i in xrange(5):
        random.shuffle(cases)
        for name, output in cases:
            print "Go to position %s" % name
            rospy.sleep(1)
            print "Snappshotting in 2s"
            rospy.sleep(2)

            with myo_data_lock:
                trainSet.addSample(myo_data, output)
            print "Snapshot taken"
            rospy.sleep(1)
            
    emg_sum.unsubscribe()

    print "Starting Training"

    trainer = BackpropTrainer(net, trainSet)

    trainer.trainUntilConvergence()

    print "Training Completed"

    
