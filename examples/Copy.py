#!/usr/bin/env python

import signal
import time
import sys

from pirc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

print("Starting")
while run:
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    aKeyValue = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    if not error:
        print("Card read UID {:02x}{:02x}{:02x}{:02x}: ".format(uid[0], uid[1], uid[2], uid[3]))
        if rdr.select_tag(uid):
            for i in range(16):
                if rdr.card_auth(rdr.auth_b, i*4+3, aKeyValue, uid):
                    for j in range(4):
                        print("data for block {} : \n".format(i*4 + j))
                        ret, data = rdr.read(i*4 + j)
                        if ret:
                            print(data)
                        else:
                            print("read error ... ")
                        print('\n')
                else:
                    print("card auth failed! \n")
        else:
            print("select tag failed! \n")

    time.sleep(1)

        # print("Setting tag")
        # util.set_tag(uid)
        # print("\nAuthorizing")
        # #util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
        # util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
        # print("\nReading")
        # util.read_out(4)
        # print("\nDeauthorizing")
        # util.deauth()
        #
        # time.sleep(1)
