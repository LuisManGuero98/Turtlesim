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



def desplazamiento_x(distancia):
    global x
    global y
    global theta

    velocity_message = Twist()
    cmd_vel_topic = '/turtle1/cmd_vel'
    time.sleep(1.0)
    n=distancia+x

    while(True):
        linear_speed = 1

        velocity_message.linear.x = linear_speed
        velocity_publisher.publish(velocity_message)

        if (x > n):
            break

def poligono (radio,lados):
    global x
    global y
    global theta
    total=0

    velocity_message = Twist()
    cmd_vel_topic = '/turtle1/cmd_vel'

    grados=360/lados
    #grados=180-grados
    #grados=360-grados
    #grados=grados/2
    rad=(grados*math.pi)/180

    print ('grados = ', grados)
    print ('radianes = ', rad)


    #longi=math.sqrt((2*radio*radio)-(2*radio*radio*math.cos(rad)))

    a2=2*radio*radio
    b2=2*radio*radio
    co=math.cos(rad)

    bco=b2*co
    print('a2 = ', a2)
    print('b2 = ', b2)
    print('co = ', co)
    longi=math.sqrt(a2-bco)
    longi=longi+0.1

    print('longitud = ', longi)
    time.sleep(1.0)

    velocity_message.angular.z = math.pi/2
    velocity_publisher.publish(velocity_message)
    time.sleep(1.0)
    velocity_message.angular.z = 0

    velocity_message.linear.x = longi
    velocity_publisher.publish(velocity_message)
    time.sleep(5.0)
    velocity_message.linear.x = 0

    while(True):

        velocity_message.angular.z = rad+0.005
        velocity_publisher.publish(velocity_message)
        time.sleep(1.0)
        velocity_message.angular.z = 0

        velocity_message.linear.x = longi
        velocity_publisher.publish(velocity_message)
        time.sleep(5.0)
        velocity_message.linear.x = 0

        total=total+1
        print('Total = ', total)
        #time.sleep(1.0)

        if(total==lados-1):
            break

def go_to_goal (radio,lados):

    #Circulo radio 4
    print('Desplazamiento')
    desplazamiento_x(radio)
    print('Poligono')
    time.sleep(2.0)
    poligono(radio,lados)


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
	go_to_goal(4,50) #radio,lados
	time.sleep(1.0)

    except rospy.ROSInterruptException:
	pass
