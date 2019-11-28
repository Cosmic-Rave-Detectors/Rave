#import RPi.GPIO as g
import time
from time import sleep
import numpy as np
import csv
#import sys
import tkinter as tk
from tkinter import ttk

#g.setmode(g.BCM)
#g.setup(22, g.IN, pull_up_down=g.PUD_DOWN)

revcount = 0
ready = False
count = 0
tim = 0
rate = 0
data_bank=[]
#starttime = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
#rise = g.add_event_detect(22,g.RISING)

#def increaserev(channel): #Every count increase the variable by one
# global revcount
# revcount +=1
#
#def main():  
#    global ready
#    ready = True
#    try:
#        while ready == True:
#            global tim
#            global rate
#            global revcount
#            global starttime          
#            if g.event_detected(22): #Detects pulse and waits to ensure it is a sent pulse and not noise
#                sleep(0.000001)               
#                if g.input(22) == 1: #If still high, increments counter
#                    increaserev(22)                    
#            currenttime = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)        
#            if currenttime >= starttime + 5: #Every 5 seconds the average is calculated
#                tim += 5
#                #count = revcount/tim #rate = revcount/(time-revcount*pulse width(200um))
#                rate = revcount/(currenttime -revcount*16*10**(-6))
#                #print ("Average count rate over {0} seconds: {1} Hz:D".format(tim, rate))
#                data_bank.append(rate)
#                print(data_bank)
#                starttime = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)             
#            with open('data_bank.csv', 'w') as csvFile:
#                writer = csv.writer(csvFile)
#                writer.writerow(data_bank)
#                  
#    except KeyboardInterrupt:
#        csvFile.close()
#        pass
#         
#if __name__ == "__main__":
#    main()
    
filenameuser = "DefaultName"

    
class PulseGUI:
    
    '''
    This class contains all of the functions needed for the user to control the GUI and the experiment
    '''
    
    def __init__(self, window):
        #User can change file name here
        ttk.Label(window, text = "File name:").grid(sticky = 'NESW', padx = 10)
        self.filenameuser = tk.StringVar()
        self.filenameuser = tk.Entry(window)
        self.filenameuser.grid(sticky = 'NESW', row = 0, column = 1, columnspan = 2, padx = 10)
        
        self.StartButton = ttk.Button(window, text = "Start Data Collection",
                                      command = self.user_params)
        self.StartButton.grid(sticky = 'NESW', row = 10, column = 1, pady = 10)
        
        self.StopButton = ttk.Button(window, text = "Stop Data Collection",
                                     command = self.stop)
        self.StopButton.grid(sticky = 'NESW', row = 10, column = 2, pady = 10)
        
    def user_params(self): #Calls this once a button is pressed to update parameters
        if not ready:
            global filename
            if len(self.filenameuser.get()) != 0:
                filename = self.filenameuser.get()
            
            main()
                
        else:
            print('Data is already being collected!')
            
    def stop(self): #This function switches the program to a "not ready" state
        global ready
        global datacollect
        
        if not ready:  #This is called from main function
            datacollect = False
            print('Experiment Stopped')
            pass
        else: #Called when user hits Stop Experiment
            ready = False
            datacollect = False
            print('Experiment Stopped')

    
    
    


window = tk.Tk()
window.geometry("700x300")
window.title('Cosmic Rave Detectors')
Rave = PulseGUI(window)

window.mainloop()