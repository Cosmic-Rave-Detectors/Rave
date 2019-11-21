import RPi.GPIO as g
import time
from time import sleep
import numpy as np
import csv
 
g.setmode(g.BCM)
g.setup(22, g.IN)
global revcount
global count
global rate
revcount = 0
count = 0
tim = 0
rate = 0
data_bank=[]

def increaserev(channel):
 global revcount
 revcount +=1
 
g.add_event_detect(22,g.RISING, callback=increaserev)

while True:
 sleep(5)
 tim += 5
 #count = revcount/tim #rate = revcount/(time-revcount*pulse width(200um))
 rate = revcount/(tim-revcount*136*10**(-6))
 #print ("Average count rate over {0} seconds: {1} Hz:D".format(tim, rate))
 data_bank.append(rate)
 print(data_bank)
 
 with open('data_bank.csv', 'w') as csvFile:
     writer = csv.writer(csvFile)
     writer.writerow(data_bank)
csvFile.close()
 