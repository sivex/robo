#!/usr/bin/env python2

import os
import random
import rospy
import sys
import threading

from ros_myo.msg import EmgArray

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.tools.customxml import NetworkWriter, NetworkReader

myo_data_lock = threading.Lock()
myo_data = [0.0] * 8

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

    if len(sys.argv[1:]) >= 1 and os.path.exists(sys.argv[1]):
        print "Loading from %s" % sys.argv[1]
        net = NetworkReader.readFrom(sys.argv[1])
    else:
        print "Starting new network"
        net = buildNetwork(8, 10, 2)

    trainSet = SupervisedDataSet(8, 2)

    print "Beginning Data Collection"

    for i in xrange(1):
        random.shuffle(cases)
        for name, output in cases:
            print "Go to position %s" % name
            print "press enter to continue...",
            raw_input()

            with myo_data_lock:
                print "Snapshotting data: %s" % myo_data
                trainSet.addSample(myo_data, output)
            
    emg_sub.unregister()

    print "Starting Training"

    trainer = BackpropTrainer(net, trainSet)

    trainer.trainUntilConvergence()

    print "Training Completed"

    if len(sys.argv[1:]) >= 1:
        print "Saving trained network in %s" % sys.argv[1]
        NetworkWriter.writeToFile(net, sys.argv[1])

    print "Running rest of input on network"

    def run_network(emgArr):
        print net.activate(emgArr.data)

    emg_sub = rospy.Subscriber("myo_emg", EmgArray, run_network)

    rospy.spin()

if __name__ == '__main__':
    main()
