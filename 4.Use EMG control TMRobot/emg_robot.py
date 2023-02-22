# TM Robot Part - - - - - - - - 
import rospy
from TM_Robot import TM_Robot
from tm_msgs.msg import *
from tm_msgs.srv import *
# EMG Part - - - - - - - - 
import numpy as np
import time
import time, random
import serial
from collections import deque

TM = TM_Robot([])

def EMG_control():
    
    # initial setup
    rospy.init_node('EMG_control')
    print("----------start------------")

    # Cartesian Point [unit: x(mm),y(mm),z(mm),rx(deg),ry(deg),rz(deg)]
    cp1 = [365, 470, 650, 180, 0, 155]
    TM.move_TM(cp1, Move_type='PTP_T', Speed=3.0, blend_Mode = False)

    # open serial port
    strPort='/dev/ttyACM0'  # e.g 'COM6' windows or '/dev/ttyUSB0 or /dev/ttyACM0' for linux
    ser = serial.Serial(strPort, 115200)
    ser.flush()

    temp = deque(maxlen = 20)

    while True:
        for i in range(5):
            data = float(ser.readline())
            data = data / 1024 * 3.3
            temp.append(data)

        diff = abs(data - np.mean(temp))
        print(diff)
        threshold = 0.6

        if (diff > threshold):
            grasp()
        elif (diff <= threshold):
            release()
        else:
            pass

def grasp():
    TM.set_IO(0, state = 'HIGH')
    rospy.sleep(1)

def release():
    TM.set_IO(0, state = 'LOW')

if __name__ == '__main__':
    try:
        EMG_control()
    except rospy.ROSInterruptException:
        pass