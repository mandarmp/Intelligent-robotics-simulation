#!/usr/bin/env python3

from os import path
import os
from pickle import NONE
#from my_simluations.src.transformations import pixel_to_world, world_to_pixel
import rospy
import rospkg
from std_msgs.msg import UInt16, Int8, String
from my_simluations.srv import goal as _GOAL
from my_simluations.srv import goalResponse as _GOAL_resp
from visualization_msgs.msg import MarkerArray, Marker
import time
import math
from transformations import world_to_pixel, pixel_to_world, worldtheta_to_pixeltheta, real_to_pixel, pixel_to_real, getHeading, rotateQuaternion
import actionlib
from move_base_msgs.msg import MoveBaseGoal,MoveBaseAction
from geometry_msgs.msg import Twist , Point , Quaternion, Pose, PoseWithCovarianceStamped
from actionlib_msgs.msg import *

from my_simluations.srv import tables as _TABLES

PI = 3.14159

amcl_pose = Pose()
amcl_pose_x = 0
amcl_pose_y = 0
completeAStarMap = []

threshhold = 0.2
loc_treshhold = 0.05

ROBOT_SPEED = 0.2
ANGULAR_VELOCITY = 0.4

def read_map():
    img = open('/home/josh/catkin_ws/src/my_simluations/data/cafe_map.pgm', 'rb')

    #Header values before width and height
    img.readline()
    img.readline()

    (width, height) = [int(i) for i in img.readline().split()]
    depth = int(img.readline())
    assert depth <= 255

    aStarMap = []

    for y in range(height):
        row = []
        for y in range(width):
            val = ord(img.readline(1))
            if val < 100:
                row.append(0)
            elif val == 254:
                row.append(1)
            else:
                row.append(-1)
        aStarMap.append(row)

    #print(aStarMap)
    print("map made")
    return aStarMap



class aStarNode():
    def __init__(self, parentNode = None, position = None):
        self.parentNode = parentNode
        self.position = position
        self.x = position[0]
        self.y = position[1]

        self.h = 0
        self.g = 0
        self.f = 0

    def toString(self, completeAStarMap = None):
        if completeAStarMap == None:
            return '(' + str(self.x) + ',' + str(self.y) + ') [' + str(self.g) + ',' + str(self.h) + ',' + str(self.f)+  ']'
        else:
            return '(' + str(self.x) + ',' + str(self.y) + ') [' + str(self.g) + ',' + str(self.h) + ',' + str(self.f) + '] {' + str(completeAStarMap[self.y][self.x]) + '}'


def a_star_calculation(start, end):
    completeAStarMap = read_map()
#   print(completeAStarMap)
    width = len(completeAStarMap[0])
    height = len(completeAStarMap)

    print(width)
    print(height)

    openList = []
    closedList = []

    openList.append(aStarNode(None, (start['x'], start['y'])))

    while not (len(openList) == 0 or len(openList) > 10000000):

        currentNode = openList[0]
        currentNodeNum = 0

        for i in range(len(openList)):
            if openList[i].f < currentNode.f:
                currentNode = openList[i]
                currentNodeNum = i

        openList.pop(currentNodeNum)
        closedList.append(currentNode)

  #      print('Start Node: (' + str(start['x']) + ',' + str(start['y']) + ')')
 ##       print('End Node: (' + str(end['x']) + ',' + str(end['y']) + ')')
        print('Current Node: (' + str(currentNode.x) + ',' + str(currentNode.y) + ')')
        #print('Current Node: ' + currentNode.toString(completeAStarMap))
        #print('Size Open List: ' + str(len(openList)))
#        print('Size Closed List: ' + str(len(closedList)))
#        print()
#        print("OPEN LIST")
#        for node in openList:
#            print('(' + str(node['x']) + ',' + str(node['y']) + ')')
#        print()
#        print("CLOSED LIST")
#        for node in closedList:
#            print('(' + str(node['x']) + ',' + str(node['y']) + ')')
#        print()
#        time.sleep(1)

        if currentNode.x == end['x'] and currentNode.y == end['y']:
            path_to_end = []
            current_node = currentNode
            while current_node != None:
                path_to_end.append({'x':current_node.x, 'y':current_node.y})
                current_node = current_node.parentNode
            return path_to_end[::-1]
        else:
            children = []

            for child_position_rel in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                child_position = (currentNode.x + child_position_rel[0], currentNode.y + child_position_rel[1])

                if child_position[0] < 0 or child_position[0] >= width or child_position[1] < 0 or child_position[1] >= height:
                    continue

                if completeAStarMap[child_position[1]][child_position[0]] != 1:
                    continue

                child = aStarNode(currentNode, child_position)
                child.parent = currentNode

#                print(child.toString())
                children.append(child)

#            if currentNode['x'] > 0:
#                if currentNode['y'] > 0:
#                    children.append(a_star_nodes[x-1][y-1])
#                if currentNode['y'] < height - 1:
#                    children.append(a_star_nodes[x-1][y+1])
#            if currentNode['x'] < width - 1:
#                children.append(a_star_nodes[x+1][y])
#                if currentNode['y'] > 0:
#                    children.append(a_star_nodes[x+1][y-1])
#                if currentNode['y'] < height - 1:
#                    children.append(a_star_nodes[x+1][y+1])
#            if currentNode['y'] > 0:
#                children.append(a_star_nodes[x][y-1])
#            if currentNode['y'] < height - 1:
#                children.append(a_star_nodes[x][y+1])

            for i in range(len(children)):
                skip = False
                for node in closedList:
                    if node.x == children[i].x and node.y == children[i].y:
                        skip = True
                        break

                if skip:
                    continue

                children[i].g = currentNode.g + math.hypot(children[i].x - currentNode.x, children[i].y - currentNode.y)
                children[i].h = math.hypot(end['x'] - children[i].x, end['y']-children[i].y)
                children[i].f = children[i].g + children[i].h

                for open_node in openList:
                    if open_node.x == children[i].x and open_node.y == children[i].y:
                        if children[i].g >= open_node.g:
                            skip = True
                            break

                if skip:
                    continue

                openList.append(children[i])



def a_star_cleanup(aStarNodes):
    completeAStarMap = read_map()
    width = len(completeAStarMap[0])
    height = len(completeAStarMap)

    toKeep = [0]
    nextI = 0

    for i in range(len(aStarNodes)):
        complete = False
        if i == nextI:
            for j in (range(i+1, len(aStarNodes))):
                nodeOne = aStarNodes[i]
                nodeTwo = aStarNodes[j]

                trajectoryNormalise = (math.hypot(nodeOne['x'] - nodeTwo['x'], nodeOne['y']-nodeTwo['y']) / 10)
                trajectory = (int((nodeTwo['x'] - nodeOne['x']) / trajectoryNormalise),int((nodeTwo['y'] - nodeOne['y']) / trajectoryNormalise))

                if trajectory[0] != 0 and trajectory[1] != 0:
                    for x in range(nodeOne['x'] + 2, nodeTwo['x'], int(trajectory[0])):
                        for y in range(nodeOne['y'] + 2, nodeTwo['y'], int(trajectory[1])):
                            if completeAStarMap[int(y)][int(x)] != 1:
                                toKeep.append(j - 1)
                                nextI = j - 1
                                complete = True
                                break

                        if complete:
                            break
                elif trajectory[0] == 0:
                    for y in range(nodeOne['y'] + 2, nodeTwo['y'], int(trajectory[1])):
                        if completeAStarMap[int(y)][int(nodeOne['x'] )] != 1:
                            toKeep.append(j - 1)
                            nextI = j - 1
                            complete = True
                            break
                elif trajectory[1] == 0:
                    for x in range(nodeOne['x'] + 2, nodeTwo['x'], int(trajectory[0])):
                        if completeAStarMap[int(nodeOne['y'])][int(x)] != 1:
                            toKeep.append(j - 1)
                            nextI = j - 1
                            complete = True
                            break

                if complete:
                    break

    clean_a_star = []
    for i in toKeep:
        clean_a_star.append(aStarNodes[i])
    clean_a_star.append(aStarNodes[len(aStarNodes) -1])

    return clean_a_star

def amcl_callback(msg):
    #print("inside amcl callback")
    global amcl_pose_x
    global amcl_pose_y
    global amcl_pose
    amcl_pose = msg.pose.pose
    amcl_pose_x, amcl_pose_y = real_to_pixel(msg.pose.pose.position.x,msg.pose.pose.position.y)
    #print(getHeading(amcl_pose.orientation)+PI)
    #print(amcl_pose)


def rotate_bot(_goal_heading):
    curr_heading = getHeading(amcl_pose.orientation)+PI
    turn = Twist()
    goal_heading = _goal_heading+PI
    print(curr_heading)
    print(goal_heading)
    #print(goal_heading-goal_heading*0.1)
    #global amcl_pose
    while curr_heading > goal_heading+goal_heading*0.1 or curr_heading < (goal_heading-goal_heading*threshhold):
        #print("rotating")
        #msg = rospy.wait_for_message('/amcl_pose',PoseWithCovarianceStamped, timeout=None)
        curr_heading = getHeading(amcl_pose.orientation)+PI
        #print(curr_heading)
        #print(str(goal_heading+goal_heading*threshhold)+str(";")+str(goal_heading)+str(";")+str(goal_heading-goal_heading*threshhold))
        ratio = abs(curr_heading-goal_heading)
        #turn.angular.z = ANGULAR_VELOCITY
        turn.angular.z = min(ANGULAR_VELOCITY, ANGULAR_VELOCITY*ratio)
        move.publish(turn)

def euclidean_distance(_x,_y, _x_prev,_y_prev):

	return math.sqrt(math.pow((_x-_x_prev),2) + math.pow((_y-_y_prev),2))

def move_to_loc(x,y,x_prev, y_prev):
    forward = Twist()
    while (((amcl_pose_x > x+ x*loc_treshhold) or (amcl_pose_x < x- x*loc_treshhold)) or (((864 -amcl_pose_y)  > y+ y*loc_treshhold) or ((864-amcl_pose_y) < y- y*loc_treshhold))):
        #print("moving")
        #rint(str(amcl_pose_y))
        #print(str(y+ y*loc_treshhold)+str(";")+str(y)+str(";")+str(y- y*loc_treshhold))
        #print(str(amcl_pose_x))
        #print(str(x+ x*loc_treshhold)+str(";")+str(x)+str(";")+str(x- x*loc_treshhold))
        divergence = (abs((x-x_prev)*(y_prev-amcl_pose_y)-(x_prev-amcl_pose_x)*(y-y_prev)))/(math.sqrt(((x-x_prev)**2)+((y-y_prev)**2)))
        #print(divergence)
        if (divergence > 20):
            inc_x = x - amcl_pose_x
            inc_y = y - amcl_pose_y
            #print(inc_x)
            #print(inc_y)
            angle_to_goal = math.atan2(inc_y, inc_x)
            rotate_bot(angle_to_goal)
        dist = euclidean_distance(x,y,x_prev, y_prev)/10
        forward.linear.x = min(ROBOT_SPEED,ROBOT_SPEED*dist)
        move.publish(forward)
    forward.linear.x = 0
    move.publish(forward)


def go_to_place(req):
    time.sleep(3)
    x,y= real_to_pixel(req.x,req.y)
    yaw= req.yaw

    end = {'x':x,'y':y}
    start = None
    #get the start pose from amcl
    global amcl_pose_x
    global amcl_pose_y
    global amcl_pose
    #print(amcl_pose)
    if amcl_pose is not None:
        #print("inside amcl_pose not NONE")
        #_x_,_y_ = real_to_pixel(amcl_pose.position.x,amcl_pose.position.y)
        start= {'x': amcl_pose_x,'y': amcl_pose_y}
    print(start)
    print(end)

    paths =a_star_calculation(start,end)
    paths = a_star_cleanup(paths)
    print(paths)

    previous_coordinate = amcl_pose
    twist = Twist()
    twist.linear.x = ROBOT_SPEED
    pose_goal = Pose()
    for i,coordinate in enumerate(paths):
        if i > 0:
            #rospy.loginfo("Navigating to pose",coordinate)
            #the coordinates are in pixel
            # world_points =pixel_to_world((coordinate['x'],coordinate['y']),image_size)
            # success = navigate(world_points[0],world_points[1],amcl_pose.orientation)
            print(previous_coordinate)
            inc_x = int(coordinate['x']) - amcl_pose_x
            inc_y = int(coordinate['y']) - amcl_pose_y

            print(inc_x)
            print(inc_y)
            angle_to_goal = math.atan2(inc_y, inc_x)
            rotate_bot(angle_to_goal)
            time.sleep(1)
            print("rotated")
            move_to_loc(int(coordinate['x']),int(coordinate['y']),previous_coordinate['x'],previous_coordinate['y'])
            print("moved")
            previous_coordinate = coordinate
        else:
            previous_coordinate = coordinate
            print("skipped")




    # print("AMCL pose:")
    # print(amcl_pose)
    # print("At destination:")
    # print("x: " +str(req.x))
    # print("y: " +str(req.y))
    # print("yaw: " +str(req.yaw))
    return _GOAL_resp(100)



if __name__ == "__main__":
    rospy.init_node("pathfinder")
    rospy.loginfo("hello from pathfinder")
    s = rospy.Service("path", _GOAL, go_to_place)
    move = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.Subscriber('/amcl_pose',PoseWithCovarianceStamped,amcl_callback)
    print("started")
    rospy.spin()
