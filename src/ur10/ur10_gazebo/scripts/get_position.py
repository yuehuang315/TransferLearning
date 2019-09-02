#!/usr/bin/python
#
# Get end-effector position values from gazebo using messages
#

# rosservice list
# rosservice call /gazebo/get_model_state "robot" "wrist_3_link"

import rospy
from gazebo_msgs.srv import GetLinkState
from gazebo_msgs.srv import GetJointProperties

rospy.wait_for_service('/gazebo/get_link_state')
rospy.wait_for_service('/gazebo/get_joint_properties')
model_coordinates = rospy.ServiceProxy( '/gazebo/get_link_state', GetLinkState)
model_angle = rospy.ServiceProxy( '/gazebo/get_joint_properties', GetJointProperties)

def pos_main():
	object_coordinates = model_coordinates("wrist_3_link", "world")
	z_position = object_coordinates.link_state.pose.position.z
	y_position = object_coordinates.link_state.pose.position.y
	x_position = object_coordinates.link_state.pose.position.x
	print("position",x_position,y_position,z_position+0.6)
	return x_position,y_position,z_position+0.6
		# object_joint_shoulder_pan = model_angle("shoulder_pan_joint")
		# object_joint_shoulder_lift = model_angle("shoulder_lift_joint")
		# object_joint_elbow = model_angle("elbow_joint")
		# object_joint_wrist_1 = model_angle("wrist_1_joint")
		# object_joint_wrist_2 = model_angle("wrist_2_joint")
		# object_joint_wrist_3 = model_angle("wrist_3_joint")

		# print("angle",object_joint_shoulder_pan.position, 
		# 	object_joint_shoulder_lift.position, object_joint_elbow.position,
		# 	object_joint_wrist_1.position, object_joint_wrist_2.position, 
		# 	object_joint_wrist_3.position)

if __name__ == '__main__':
	try:
		pos_main()
	except rospy.ServiceException as exc:
		print("Service did not process request: " + str(exc))
