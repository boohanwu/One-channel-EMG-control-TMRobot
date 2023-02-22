# TM Robot Use - - - - - - - - 
import rospy
from TM_Robot import TM_Robot
from tm_msgs.msg import *
from tm_msgs.srv import *

TM = TM_Robot([])

def EMG_control():

    rospy.init_node('EMG_control')
    print("----------start------------")
        
    key = input("")

    # -------- Set Points -------- #
    # Joint Angle: J1~J6 [unit:degree]
    jp1 = [180,0,90,0,90,0]

    # Cartesian Point [unit: x(mm),y(mm),z(mm),rx(deg),ry(deg),rz(deg)]
    cp1 = [-517.99,122.65,500,180,0,-90]
    cp2 = [-480,122.65,500,180,0,-90]

    while not rospy.is_shutdown():
        if key == "0":  #Example

            # --------Action Start--------- # 
            # Move to joint_point 1 by PTP_J   
            TM.move_TM(jp1, Move_type='PTP_J', Speed = 3.0, blend_Mode = False)  

            # Grip things for 3 seconds
            TM.set_IO(0,state = 'HIGH')
            rospy.sleep(3)
            TM.set_IO(0,state = 'LOW')

            # Move to cartesian_point 1 by PTP_T
            TM.move_TM(cp1, Move_type='PTP_T', Speed=3.0, blend_Mode = False) 
            # Move to point 3 by LINE_T
            TM.move_TM(cp2, Move_type='LINE_T', Speed=3.0, blend_Mode = False) 
            # --------Action End--------- # 
            
            key = input("")
            continue

        elif key == "1": 

            # --------Action Start--------- # 






            # --------Action End--------- # 

            key = input("")
            continue

        elif key == "2":

            # -------Action Start--------- # 






            #--------Action End---------# 
            
            key = input("")
            continue
        else:
            break
    

if __name__ == '__main__':
    try:
        EMG_control()
    except rospy.ROSInterruptException:
        pass