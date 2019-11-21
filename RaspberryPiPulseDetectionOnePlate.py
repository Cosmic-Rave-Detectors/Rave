import RPi.GPIO as g
import time
from time import sleep
import numpy as np
import csv
import sys

g.setmode(g.BCM)
g.setup(22, g.IN, pull_up_down=g.PUD_DOWN)

revcount = 0
count = 0
tim = 0
rate = 0
data_bank=[]
starttime = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
rise = g.add_event_detect(22,g.RISING)

def increaserev(channel):
 global revcount
 revcount +=1

def main():  
    try:
        while True:
            global tim
            global rate
            global revcount
            global starttime
           
            if g.event_detected(22):
                sleep(0.000001)
                
                if g.input(22) == 1:
                    increaserev(22)
                    
            currenttime = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
        
            if currenttime >= starttime + 5:
                tim += 5
                #count = revcount/tim #rate = revcount/(time-revcount*pulse width(200um))
                rate = revcount/(currenttime -revcount*16*10**(-6))
                #print ("Average count rate over {0} seconds: {1} Hz:D".format(tim, rate))
                data_bank.append(rate)
                print(data_bank)
                starttime = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
             
            with open('data_bank.csv', 'w') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(data_bank)
                   
    except KeyboardInterrupt:
        csvFile.close()
        pass
         
if __name__ == "__main__":
    main()
    
    
    
##fall = g.add_event_detect(22,g.FALL)



##while True:
## sleep(5)
## tim += 5
## #count = revcount/tim #rate = revcount/(time-revcount*pulse width(200um))
## rate = revcount/(tim-revcount*16*10**(-6))
## #print ("Average count rate over {0} seconds: {1} Hz:D".format(tim, rate))
## data_bank.append(rate)
## print(data_bank)
## 
## with open('data_bank.csv', 'w') as csvFile:
##     writer = csv.writer(csvFile)
##     writer.writerow(data_bank)
##csvFile.close()
