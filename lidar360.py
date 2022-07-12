#!/usr/bin/env python3

# to be used with 360-degree LiDAR device (LD06)
# read here: https://www.ldrobot.com/editor/file/20210422/1619071627351038.pdf
# on average: 4500 points/sec, 10 revs/sec

from queue import Queue
import serial
from threading import Thread
import time

PACKET_LEN = 47
NUM_POINTS = 12

class Point:
    def __init__(self, angle, dist, conf=None, timestamp=None):
        self.angle = angle
        self.dist = dist
        self.conf = conf
        self.timestamp = timestamp

    def __str__(self):
        return "Angle: %.2f deg\nDistance: %.3f m\nConfidence: %s\nTime: %d ms"\
            % (self.angle,\
               self.dist, \
               ("N/A" if self.conf is None else str(self.conf)),\
               ("N/A" if self.timestamp is None else str(self.timestamp)))

class LidarKit:
    def __init__(self, addr):
        self._addr = addr
        self._baud = 230400
        self.points = Queue()
        self.is_running = False
        self._thread = None
        #if not self._ser.isOpen():
        #    ser.open()

    def _thread_loop(self):
        ser = serial.Serial(self._addr, self._baud, timeout=1.0)
        if not ser.isOpen():
            ser.open()
        while self.is_running:
            #print("1")
            counter = ser.in_waiting
            if counter >= 1:
                #print("2")
                bytes_serial = bytearray(ser.read(1))
                if bytes_serial[0] == 0x54:
                    bytes_left = PACKET_LEN - 1
                    while bytes_left > 0:
                        if not self.is_running:
                            ser.close()
                            return
                        bytes_read = ser.read(bytes_left)
                        bytes_serial.extend(bytes_read)
                        bytes_left -= len(bytes_read)
                        #print("Read: %d, Left: %d" % (len(bytes_read), bytes_left))
                    #print(bytes_serial.hex())
                    #ser.reset_input_buffer()
                    
                    data_len = bytes_serial[1] & 0b11111
                    #bytes_serial = ser.read(data_len + 1)
                
                    radar_speed = bytes_serial[2] + 256*bytes_serial[3]
                    start_angle = (bytes_serial[4] + 256*bytes_serial[5]) / 100.0
                    end_angle = (bytes_serial[42] + 256*bytes_serial[43]) / 100.0
                    timestamp = bytes_serial[44] + 256*bytes_serial[45]
                    
                    #distances = []
                    #confidences = []
                    #angles = []
                    
                    step = (end_angle - start_angle) / (NUM_POINTS - 1)
                    for i in range(0, NUM_POINTS):
                        j = 6 + 3*i
                    
                        this_dist = (bytes_serial[j] + 256*bytes_serial[j+1]) / 1000.0
                        this_conf = bytes_serial[j+2]
                        this_angle = start_angle + i*step

                        p = Point(this_angle, this_dist, this_conf, timestamp)
                        self.points.put(p)
                        
                        
                        #distances.append(this_dist)
                        #confidences.append(this_conf)
                        #angles.append(this_angle)
                    
                    #print("Radar speed (deg/s): %d" % radar_speed)
                    #print("Start angle (deg): %.2f" % start_angle)
                    #print("End angle (deg): %.2f" % end_angle)
                
                    #for (d,c,a) in zip(distances, confidences, angles):
                        #print("Angle = %.2f deg" % a)
                        #print("Distance = %.2f m" % d)
                        #print("Confidence = %d" % c)
                        #print("")
                        #if a > 360.0:
                            #print("Bad angle!")
                            #exit(0)
                        
            #else:
            #print("Bad packet")
                
        #else:
        #print("No data")

    def start(self):
        self.is_running = True
        if (self._thread is None) or (not self._thread.is_alive()):
            self._thread = Thread(target=self._thread_loop)
        self._thread.start()

    def stop(self):
        self.is_running = False
        self._thread.join()

    def __del__(self):
        self.is_running = False
        #if self._ser.isOpen():
        #    self._ser.close()

if __name__ == '__main__':
    try:
        lk = LidarKit('/dev/ttyUSB0')
        lk.start()
        time.sleep(1.0)
        lk.stop()
        print(lk.points.get(0))
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
            print("Program interrupted by user.")
