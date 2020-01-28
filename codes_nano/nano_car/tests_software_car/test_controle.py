import time
import os

import board
import busio
import time
from approxeng.input.selectbinder import ControllerResource

while True:
       with ControllerResource() as joystick:
           print(type(joystick).__name__)
           while joystick.connected:
                time.sleep(0.1)
                os.system('clear')
                

                axis_list = [ 'lx', 'ry','rx' ]

                for axis_name in axis_list:                  
                    if  axis_name == 'lx' :
                        a = joystick[axis_name]
                        b = (a+1)/2*1
                        print("Direcao",b)

                    if  axis_name == 'ry' :
                        c = joystick[axis_name]
                        d = ((c*(-1))+1)/2*0.5
                        print("ry",d)

                    if  axis_name == 'rx' :
                        e = joystick[axis_name]
                        f = ((e*(-1))+1)/2*0.5
                        print("rt",f) 
                        g = d+f
                        print("Acelerador",g)
                  


"""
controls=[
                                             Button("Circle", 305, sname='circle'),#'square'
                                             Button("Cross", 304, sname='cross'),
                                             Button("Square", 308, sname='square'),
                                             Button("Triangle", 307, sname='triangle'),
                                             Button("Home (PS)", 316, sname='home'),
                                             Button("Share", 314, sname='select'),
                                             Button("Options", 315, sname='start'),
                                             Button("Trackpad", 'touch272', sname='ps4_pad'),
                                             Button("L1", 310, sname='l1'),
                                             Button("R1", 311, sname='r1'),
                                             Button("L2", 312, sname='l2'),
                                             Button("R2", 313, sname='r2'),
                                             Button("Left Stick", 317, sname='ls'),
                                             Button("Right Stick", 318, sname='rs'),
                                             CentredAxis("Left Horizontal", 0, 255, 0, sname='lx'),
                                             CentredAxis("Left Vertical", 0, 255, 1, invert=True, sname='ly'),
                                             CentredAxis("Right Horizontal", 0, 255, 2, sname='rx'),
                                             CentredAxis("Right Vertical", 0, 255, 5, invert=True, sname='ry'),#ry
                                             TriggerAxis("Left Trigger", 0, 255, 3, sname='lt'),
                                             TriggerAxis("Right Trigger", 0, 255, 4, sname='rt'),#rt
                                             BinaryAxis("D-pad Horizontal", 16, b1name='dleft', b2name='dright'),
                                             BinaryAxis("D-pad Vertical", 17, b1name='dup', b2name='ddown'),
                                             # CentredAxis("Motion 3", -1, 1, 'motion3', sname='zm3'),
                                             CentredAxis("Yaw rate", -2097152, 2097152, 'motion4', sname='yaw_rate',
                                                         invert=True),
                                             # CentredAxis("Motion 5", -1, 1, 'motion5', sname='zm5'),
                                             CentredAxis("Roll", -8500, 8500, 'motion0', sname='roll', invert=True),
                                             # CentredAxis("Motion 1", -1, 1, 'motion1', sname='zm1'),
                                             CentredAxis("Pitch", -8500, 8500, 'motion2', sname='pitch',
                                                         invert=True),
                                             CentredAxis("Touch X", 0, 1920, 'touch53', sname='tx'),
                                             CentredAxis("Touch Y", 0, 942, 'touch54', sname='ty', invert=True)

                                         ],
"""


