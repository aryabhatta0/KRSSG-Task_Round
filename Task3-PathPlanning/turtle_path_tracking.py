#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
import socket

class TurtleBot:

    def __init__(self, path,turtle):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

        self.path = path
        self.turtle = turtle 

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
        """Moves the turtle to the goal."""
        goal_pose = Pose()
        vel_msg = Twist()
        distance_tolerance = 0.01
        
        print("Inside Class: ", self.path)
        for point in self.path:

            goal_pose.x = point[0] / 30
            goal_pose.y = (300 - point[1]) / 30
            '''
            if point[1] < 150:
                goal_pose.y = point[1] / 30 + 10
            else:
                goal_pose.y = point[1] / 30 - 10
            '''

            while self.euclidean_distance(goal_pose) >= distance_tolerance:

                # Porportional controller.

                # Linear velocity in the x-axis.
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

                # Angular velocity in the z-axis.
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)

                # Publishing our vel_msg
                self.velocity_publisher.publish(vel_msg)

                # Publish at the desired rate.
                self.rate.sleep()
                
                self.turtle.send(str(point).encode())

            # Stopping our robot after the movement is over.
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)

            # If we press control + C, the node will stop.
            #rospy.spin()
        

if __name__ == '__main__':
    try:
        #connecting to the rrt algo
        port = 5555
        turtle = socket.socket()
        turtle.connect(('localhost',port))
        print('Connection established...')
        
        path = turtle.recv(10000).decode()
        path = eval(path)
        print("Outside Class: ",path)


        x = TurtleBot(path,turtle)
        x.move2goal()
    except rospy.ROSInterruptException:
        pass
