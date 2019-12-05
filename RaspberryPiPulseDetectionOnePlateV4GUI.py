import RPi.GPIO as g
import time
from time import sleep
import numpy as np
import csv
import sys
import tkinter as tk
from tkinter import ttk
import threading

g.setmode(g.BCM)
g.setup(22, g.IN, pull_up_down=g.PUD_DOWN)

revcount = 0
ready = False
datacollect = False
done = False
filename = "DefaultName"
runtime = 5
angle = 0
count = 0
tim = 0
rate = 0
data_bank=[]
rise = g.add_event_detect(22,g.RISING)

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
        
        ttk.Label(window, text = "Cronkin' Time:").grid(sticky = 'NESW', padx = 10)
        self.runtimeuser = tk.IntVar()
        self.runtimeuser = tk.Entry(window)
        self.runtimeuser.grid(sticky = 'NESW', row = 1, column = 1, columnspan = 2, padx = 10)
        
        ttk.Label(window, text = "Angle of detector").grid(sticky = 'NESW', padx = 10)
        self.angleuser = tk.IntVar()
        self.angleuser = tk.Entry(window)
        self.angleuser.grid(sticky = 'NESW', row = 2, column = 1, columnspan = 2, padx = 10)
        
        self.StartButton = ttk.Button(window, text = "Start Data Collection",
                                      command = self.user_params)
        self.StartButton.grid(sticky = 'NESW', row = 10, column = 1, pady = 10)
        
        self.StopButton = ttk.Button(window, text = "Stop Data Collection",
                                     command = stop)
        self.StopButton.grid(sticky = 'NESW', row = 10, column = 2, pady = 10)
        
        
    def user_params(self): #Calls this once a button is pressed to update parameters
        if not ready:
            global filename
            global runtime
            global angle
            if len(self.filenameuser.get()) != 0:
                filename = self.filenameuser.get()
            if len(self.runtimeuser.get())!= 0:
                runtime = int(self.runtimeuser.get())
            if len(self.angleuser.get()) != 0:
                angle = float(self.angleuser.get())
            
            Begin_Exp(runtime)
                
        else:
            print('Data is already being collected!')

def increaserev(channel): #Every count increase the variable by one
    global revcount
    global done
    revcount +=1
    if done == True:
        revcount = 0
        done = False
 
def Begin_Exp(runtime): #
    global ready
    global starttime
    ready = True
    print('Is this the angle you want?????? {0}'.format(angle))
    starttime = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
    print('Experiment Ready')


def ExpRunning():  #Starts this experiment and opens files
    global ready
    global filename
    global csvFile
    global datacollect
    global threadon
    global threadmade
    if ready:
        csvFile = open('{0}.csv'.format(filename), 'a')
        ready = False
        datacollect = True
        threadon = False
        threadmade = False
        window.after(0,DataCollection(csvFile))
    
    window.after(1000,ExpRunning)
         
         
    
def DataCollection(csvFile): #Contains the experimental loop and begins the threading
    global datacollect
    global ready
    global rate
    global data_bank
    global done
    global currenttime
    global intervaltime
    global starttime
    global threadon
    global threadmade
    global x
    intervaltime = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
    print('Experiment started at {0:.2f}'.format(intervaltime))
    if datacollect == True:
        def detection(): #This is the thread loop that has the experiment loop
            global intervaltime
            threadon = True
            detect = False
            done = False
            while not done: #Ensures that it is always looping after the detection of signals
                while not detect:
                    if g.event_detected(22): #Detects pulse and waits to ensure it is a sent pulse and not noise
                        #sleep(0.000001)               
                        #if g.input(22) == 1: #If still high, increments counterimport numpy as np

                        detect = True
                        increaserev(22)
                    currenttime = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
                    #print('Current time: {0}s, Interval time: {1}'.format(currenttime, intervaltime))
                detect = False
                if currenttime >= intervaltime + 5: #Every 5 seconds the average is calculated
                    timediff = currenttime - starttime
                    print('Current time: {0:.2f}s'.format(timediff))
                    rate = revcount/(timediff -revcount*190*10**(-9))
                    data_bank.append(rate)
                    intervaltime = time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
                    
                    if currenttime >= starttime+int(runtime): #Stops experiment once the time taken is larger than the experiment run time specified
                        datacollect = False
                        done = True
                        writer = csv.writer(csvFile)
                        uncert = np.sqrt(revcount)/currenttime
                        datalist = []
                        datalist.append([angle, data_bank[-1], uncert])
                        print(datalist)
                        writer.writerows(datalist)
                        stop()
                        print('Count rate over {0:.4f} seconds: {1:.2f} +/- {3:.1f}\nTotal counts: {2:1d} '.format(timediff, rate, revcount, uncert))
                        print('Experiment Completed')
                        return
                    
            
        if threadmade == False: #Ensures only one thread is made
            x = threading.Thread(target=detection)
            threadmade = True
        if threadon == False: #Ensures only one thread is started
            x.start()

def stop(): #This function switches the program to a "not ready" state
        global ready
        global datacollect
        global csvFile
        global thread
        global done
        global detect
        detect = True
        done = True
        window.after_cancel(DataCollection)
        window.after_cancel(ExpRunning)
        csvFile.close()
        if not ready:  #This is called from main function
            datacollect = False
            print('Experiment Stopped')
            pass
        else: #Called when user hits Stop Experiment
            ready = False 
            datacollect = False
            print('Experiment Stopped')
    

def properclose():
    global datacollect
    global detect
    global csvFile
    global done
    global intervaltime    
    window.after_cancel(ExpRunning)
    window.after_cancel(DataCollection)
    csvFile.close()
    detect = True
    done = True
    if datacollect == True:
        print('Experiment abruptly halted {0} seconds in!'.format(intervaltime))
    window.destroy()
    

window = tk.Tk()
window.geometry("700x300")
window.title('Cosmic Rave Detectors')
Rave = PulseGUI(window)
window.after(1000, ExpRunning)
window.protocol('WM_DELETE_WINDOW', properclose)
window.mainloop()