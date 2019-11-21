import RPi.GPIO as g
import time
from time import sleep
import numpy as np
 
g.setmode(g.BCM)
g.setup(22, g.IN)
global revcount
global count 
revcount = 0
totalcount = 0
tim = 0


def increaserev(channel):
 global revcount
 revcount +=1
 
g.add_event_detect(22,g.RISING, callback=increaserev)

while True:
 sleep(5)
 tim += 5
 totalcount = revcount/tim
 print ("Average count rate over {0} seconds: {1} :D".format(tim, totalcount))
 