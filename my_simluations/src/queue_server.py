#!/usr/bin/env python3

#looks at the enqeue and dequeue requests from the ui.
# tells the robot which table to serve


from __future__ import print_function
from genpy import message
import rospy
from rospy import msg
from std_srvs.srv import Trigger, TriggerRequest, TriggerResponse
from my_simluations.srv import tables,tablesResponse
from my_simluations.srv import Queue, QueueRequest, QueueResponse
from my_simluations.srv import QueueStatus,QueueStatusResponse
from my_simluations.srv import QueueManage,QueueManageResponse
#from my_simluations.srv import Enqueue, EnqueueRequest, EnqueueResponse
#from my_simluations.srv import Dequeue, DequeueRequest, DequeueRsponse
#import queue

q1_en = []         #for enqueuing
q2_clear = []    #for dequeuing

#maintaining dicitonaries for table names and correspoding numbers

table_dict= {"Table_1": 1,"Table_2":2,"Table_3":3,"Table_4":4,"Table_5":5,"Table_6":6,"Table_7":7,"Table_8":8}
table_name = list(table_dict.keys())
table_numbers = list(table_dict.values())




def Queue_response(request):
    '''
    
    Queues and Dequeues accoridingly

    '''
    #queuing part
    msg = None
    if (request.operation==1):
        q1_en.append(table_dict[request.tablename])
        msg = "Following table added to service queue:"+ request.tablename
        success= True
    elif(request.operation ==0):
        q2_clear.append(table_dict[request.tablename])
        msg = "Following table added to clear queue:"+request.tablename
        success= True
    else:
        msg ="Invalid request"
        success = False
    print("service queue :",q1_en,"  clear queue :",q2_clear)
    return QueueResponse(success= success,msg=msg)
'''
def Manage_queues(request):
   
    if(request.type==1):
        #service done
        q1_en.remove(request.tablenumber)
        print(request.tablenumber," removed from serve queue, now :",q1_en)
    elif(request.type==0) :
        q2_clear.remove(request.tablenumber)
        print(request.tablenumber," removed from clear queue, now :",q2_clear)
    return QueueManageResponse(success=True)
'''

def PopServeNClearQueue(request):
   
    table_deliver = -1
    table_clean = -1
     #check the serve queue
    if(len(q1_en)<1): #cheking the underflow 
        print("The serve queue is empty, sending -1")
    else:
        table_deliver = q1_en.pop(0)
     #check the clear queue
    if(len(q2_clear)<1) :
        print("The clear queue is empty, sending -1")
    else:
        table_clean = q2_clear.pop(0)
    return tablesResponse(table_deliver=table_deliver,table_clean=table_clean)

def Queue_status (request):
    '''
    send the current queue status

    '''
    queuestat = [str(e) for e in q1_en]
    queuestat = ",".join(queuestat)
    
    queuestat2 =[str(e) for e in q2_clear]
    queuestat2 = ",".join(queuestat2)
    queuestat = queuestat + "|||"+queuestat2 
    return QueueStatusResponse(queuestatus=queuestat)

if __name__ == "__main__":
    rospy.init_node('queue_server')

    serv_obj = rospy.Service('/queue_server',Queue,Queue_response) #adding to the queue and dequeue
    #
    obj2 = rospy.Service('/queue_status',QueueStatus,Queue_status)

    obj3 = rospy.Service('/queuemanager',tables,PopServeNClearQueue)

    rospy.spin()
