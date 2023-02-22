import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy import signal

j = (-1)**0.5
fs = 1000

# Display loading 
class PlotData:
    def __init__(self, max_entries=50):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)

def main():
    # initial setup
    fig, (ax,ax2,ax3,ax4) = plt.subplots(4,1)
    line,  = ax.plot(np.random.randn(100))  # original data
    line2, = ax2.plot(np.random.randn(100)) # filter data
    line3, = ax3.plot(np.random.randn(100)) # frequency domain of original data
    line4, = ax4.plot(np.random.randn(100)) # frequency domain of filter data
    plt.show(block = False)
    plt.setp(line2, color = 'r')
    plt.setp(line4, color = 'r')

    PData = PlotData(500)
    ax.set_ylim(0,3.3)
    ax2.set_ylim(0,3.3)
    ax3.set_ylim(0,50)
    ax3.set_xlim(0,1000)
    ax4.set_ylim(0,50)
    ax4.set_xlim(0,1000)

    # plot parameters
    print ('plotting data...')
    # open serial port
    strPort='com7'  # e.g 'COM6' windows or '/dev/ttyUSB0' for linux
    ser = serial.Serial(strPort, 115200)
    ser.flush()

    start = time.time()
    temp = deque(maxlen = 20)

    while True:
        for ii in range(10):
            try:
                data = float(ser.readline())
                data = data / 1024 * 3.3
                
                temp.append(data)
                PData.add(time.time() - start, data)
            except:
                pass

        # 三點平均濾波器
        PData_filter = signal.lfilter([1/3,1/3,1/3], 1, PData.axis_y)    
        # Fast Fourier Transform
        xf = np.fft.fft(PData.axis_y)
        xf1 = np.fft.fft(PData_filter)
        w_hat = np.arange(0, fs, fs/len(xf))

        diff = abs(data - np.mean(temp))
        threshold = 0.3
        if (diff > threshold):
            print("Holding")
        else:
            print("Relaxing")

        ax.set_xlim(PData.axis_x[0], PData.axis_x[0] + 10)
        ax2.set_xlim(PData.axis_x[0], PData.axis_x[0] + 10)
        
        line.set_xdata(PData.axis_x)
        line.set_ydata(PData.axis_y)

        line2.set_xdata(PData.axis_x)
        line2.set_ydata(PData_filter)
        
        line3.set_xdata(w_hat[:len(xf)])
        line3.set_ydata(xf)
        
        line4.set_xdata(w_hat[:len(xf1)])
        line4.set_ydata(xf1)

        fig.canvas.draw()
        fig.canvas.flush_events()

if __name__ == '__main__':
    main()