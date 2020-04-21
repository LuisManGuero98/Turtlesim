#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

x = 0
y = 0
z = 0
theta = 0

def poseCallback(pose_message):
    global x
    global y
    global z
    global theta

    x = pose_message.x
    y = pose_message.y
    theta = pose_message.theta

def orientate (xgoal, ygoal):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle1/cmd_vel'

    while(True):
        ka = 5.0
        desired_angle_goal = math.atan2(ygoal-y, xgoal-x)
	dtheta = desired_angle_goal-theta
	angular_speed = ka * (dtheta)

        velocity_message.linear.x = 1.0
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)

        print ('x=', x, 'y=', y)

        if (dtheta < 0.01):
            break



def desplazamiento_x(distancia,condicion):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle1/cmd_vel'
    time.sleep(1.0)
    n=distancia+x
    m=x-distancia
    #print('n = ',n, 'm = ', m)
    #time.sleep(5.0)
    while(True):
        linear_speed = 1

        velocity_message.linear.x = linear_speed
        velocity_publisher.publish(velocity_message)
        print ('x=', x, 'y=', y)

        if (condicion==1):
            if (x > n):
                break

        if (condicion==2):
            if (x < m):
                break

def desplazamiento_y(distancia,condicion):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle1/cmd_vel'
    time.sleep(1.0)
    n=y+distancia
    m=y-distancia
    #print('n = ',n, 'm = ', m)
    #time.sleep(5.0)
    while(True):
        linear_speed = 1

        velocity_message.linear.x = linear_speed
        velocity_publisher.publish(velocity_message)
        print ('x=', x, 'y=', y)

        if (condicion==1):
            if (y > n):
                break

        if (condicion==2):
            if (y < m):
                break

def home (xi,yi):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle1/cmd_vel'

    print('Inicio HOME ..>')

    velocity_message.angular.z=math.pi
    velocity_publisher.publish(velocity_message)
    time.sleep(2.0)

    desplazamiento_x(xi,2)

    velocity_message.angular.z=(math.pi/2)
    velocity_publisher.publish(velocity_message)
    time.sleep(2.0)

    desplazamiento_y(yi,2)

    velocity_message.angular.z=-(3*math.pi/2)
    velocity_publisher.publish(velocity_message)
    time.sleep(2.0)

def go_to_goal (xgoal, ygoal):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle1/cmd_vel'

    #Cuadrito 8x8
    print('Desplazamiento')
    desplazamiento_x(xgoal,1)
    print('Rotacion')
    velocity_message.angular.z=(math.pi/2)
    velocity_publisher.publish(velocity_message)
    time.sleep(2.0)
    print('Desplazamiento')
    desplazamiento_y(ygoal,1)
    print('Rotacion')
    velocity_message.angular.z=(-math.pi/2)
    velocity_publisher.publish(velocity_message)
    time.sleep(2.0)
    velocity_message.angular.z=(math.pi)
    velocity_publisher.publish(velocity_message)
    time.sleep(2.0)
    print('Desplazamiento')
    desplazamiento_x(xgoal,2)
    print('Rotacion')
    velocity_message.angular.z=-(math.pi)
    velocity_publisher.publish(velocity_message)
    time.sleep(2.0)
    velocity_message.angular.z=(3*math.pi/2)
    velocity_publisher.publish(velocity_message)
    time.sleep(2.0)
    print('Desplazamiento')
    desplazamiento_y(ygoal,2)

if __name__ == '__main__':
    try:

        rospy.init_node('turtlesim_motion_pose', anonymous = True)

        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 1)

        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)
        time.sleep(2)

	
	time.sleep(2.0)
	#orientate(0,0)
	time.sleep(1.0)
	home(3.5,3.5)
	time.sleep(1.0)
	go_to_goal(8,8)
	time.sleep(1.0)

    except rospy.ROSInterruptException:
	pass
