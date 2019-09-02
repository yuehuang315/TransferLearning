#!/usr/bin/python
#
# Send joint values to UR using messages
#

import pickle
import argparse
import os
from os import path

from trajectory_msgs.msg import JointTrajectory
from std_msgs.msg import Header
from trajectory_msgs.msg import JointTrajectoryPoint
import rospy
import time
import random
import numpy as np

from get_position import pos_main

parser = argparse.ArgumentParser(description='UR10 arm data collection example')
parser.add_argument('--tag', default="default")
args = parser.parse_args()

def assets_dir():
    return path.abspath(path.join(path.dirname(path.abspath(__file__)), '..'))

def main():
    os.makedirs(os.path.join(assets_dir(), 'data', '{}_ur10_train_data'.format(args.tag)))
    rospy.init_node('send_joints') # create a publish node named send_joints
    pub = rospy.Publisher('/trajectory_controller/command',
                          JointTrajectory,
                          queue_size=10)

    # Create the topic message
    traj = JointTrajectory()
    traj.header = Header()
    # Joint names for UR
    traj.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint',
                        'elbow_joint', 'wrist_1_joint', 'wrist_2_joint',
                        'wrist_3_joint']

    rate = rospy.Rate(10)

    f_joint = open(os.path.join(assets_dir(),
        'data/{}_ur10_train_data/joint_data.txt'.format(args.tag)),"a+")
    f_end_effector = open(os.path.join(assets_dir(),
        'data/{}_ur10_train_data/end_effector_data.txt'.format(args.tag)),"a+")
    iteration = 0
    while not rospy.is_shutdown():
        traj.header.stamp = rospy.Time.now()
        pts = JointTrajectoryPoint()
        random_pos_shoulder_lift_joint = np.random.uniform(-3.14,0) # set shoulder_lift_joint angle
        random_pos = np.random.uniform(-3.14,3.14,size=(5)) # set other joints angle
        random_pos = np.insert(random_pos,1, random_pos_shoulder_lift_joint)
        print("random_pos",random_pos)
        pts.positions = random_pos
        pts.time_from_start = rospy.Duration(1.0)

        # Set the points to the trajectory
        traj.points = []
        traj.points.append(pts)
        # Publish the message
        pub.publish(traj)
        time.sleep(5)   # Delays for 5 seconds.
        x_position, y_position, z_position = pos_main()
        end_effector_position = np.array([x_position, y_position, z_position])

        # pickle store data process......
        # pickle.dump(random_pos, open(os.path.join(assets_dir(),
        #         'data/{}_ur5_train_data/joint_angle_data.pkl'.format(args.tag)), 'wb'),
        #         protocol=pickle.HIGHEST_PROTOCOL)
        # pickle.dump((x_position, y_position, z_position), open(os.path.join(assets_dir(),
        #         'data/{}_ur5_train_data/end_effector_position_data.pkl'.format(args.tag)), 'wb'),
        #         protocol=pickle.HIGHEST_PROTOCOL)
        print >> f_joint, random_pos
        print >> f_end_effector, end_effector_position

        iteration += 1
        print("iteration",iteration)
        if iteration == 1000:
            break


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print ("Program interrupted before completion")
