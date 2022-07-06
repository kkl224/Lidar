#!/usr/bin/env python3

# to be used with tfmini

import serial

ser = serial.Serial('/dev/ttyS0', 115200)

def read_data():
    while True:
        counter = ser.in_waiting
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()

            # if we get the magic signature
            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                distance = bytes_serial[2] + (256 * bytes_serial[3])
                strength = bytes_serial[4] + (256 * bytes_serial[5])
                temp = bytes_serial[6] + (256 * bytes_serial[7])
                temp = (temp / 8) - 256
                print("distance = %d" % distance)
                print("strength = %d" % strength)
                print("temperature = %d" % temp)
                ser.reset_input_buffer()
                print("")

if __name__ == '__main__':
    try:
        if not ser.isOpen():
            ser.open()
        read_data()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
            print("Program interrupted by user.")
