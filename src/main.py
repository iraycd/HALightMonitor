from os import path
import signal
import datetime
import time
from qhue import Bridge
from qhue import create_new_username
import json
import requests
from wonderwareOnline import WonderwareOnline
from wonderwareOnline import WonderwareOnlineCSV

CRED_FILE_PATH = "qhue_username.txt"
WWO_AUTH_HEADER = "/shared/WWOnlineAuthHeader.txt"

BRIDGE_IP = "192.168.1.101"

running = True

def cleanup():
  print "Cleaning up ..."

def main():
    global running
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    if not path.exists(CRED_FILE_PATH):
        while True:
            try:
                username = create_new_username(BRIDGE_IP)
                break
            except QhueException as err:
                print "Error occurred while creating a new username: {}".format(err)

        # store the username in a credential file
        with open(CRED_FILE_PATH, "w") as cred_file:
            cred_file.write(username)

    else:
        with open(CRED_FILE_PATH, "r") as cred_file:
            username = cred_file.read()

    b = Bridge(BRIDGE_IP, username)
    wonderwareOnline = WonderwareOnline('https://online.wonderware.com')

    header = ''

    with open(WWO_AUTH_HEADER, "r") as cred_file:
            header = cred_file.read()

    while running:
        startCollectingStates = datetime.datetime.now()
        lights = b.lights
        
        csv = WonderwareOnlineCSV()

        print 'Lights'
        for light in lights():
            for stateItem in lights[light]()['state']:
                if stateItem == 'xy':
                    continue
                csv.add_value(light +'.' + stateItem, lights[light]()['state'][stateItem])

            print csv.build()

            wonderwareOnline.send_csv(header, csv.build())
            if(running == False):
                break

        endCollectingStates = datetime.datetime.now()
        waitTimeInMilli = (60000000 - (endCollectingStates - startCollectingStates).microseconds) / 1000000.0
        print 'waiting '
        print waitTimeInMilli
        time.sleep(waitTimeInMilli)
        

def _handle_signal(signal, frame):
  global running

  # mark the loop stopped
  running = False
  # cleanup
  cleanup()

if __name__ == "__main__":
    main()