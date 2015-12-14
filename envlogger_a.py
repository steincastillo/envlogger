#Environment variables logger
#Program: envlogger.py
#Version 2.0
#Author: Stein Castillo
#Date: Nov 22 2015

#this program reads the environment variables: temperature, pressure and humidity
#the results will be logged to the sensefile.dat file

import time
import os
import os.path
from sense_hat import SenseHat
sense = SenseHat()

#define sensor hat display colors
r = [255, 0, 0]     #red
o = [255, 127, 0]   #orange
y = [255, 255, 0]   #yellow
g = [0, 255, 0]     #green
b = [0, 0, 255]     #black
i = [75, 0, 130]    #pink
v = [159, 0, 255]   #violet
e = [0, 0, 0]       #empty/black

#this function is used to read the cpu temperature
def cpu_temp():
    tx = os.popen('/opt/vc/bin/vcgencmd measure_temp')
    cputemp = tx.read()
    cputemp = cputemp.replace('temp=','')
    cputemp = cputemp.replace('\'C\n','')
    cputemp = float(cputemp)
    return cputemp

#Check if the log file already exists
if os.path.isfile("sensefile.dat"):
    sense.show_message("Cancelling")
    exit(0)

#set the samples and sampling rate
rate = 60            #sample frecuency in seconds
samples = 420           #number of samples
stabilization = True

#initialization read from the sensor. This is neccesary since sometimes the sensors return
#a 0 value for pressure on the first read
t = round(sense.get_temperature_from_humidity(),1)            
p = round(sense.get_pressure(),1)                              
h = round(sense.get_humidity(),1)
sense.show_letter("W")
time.sleep(5)
sense.clear()

#stabilize temperature readings by waiting 5 min
if stabilization:
    sense.show_letter("W")
    time.sleep(300)
    sense.clear()
    
#open the sampling file
sensefile = open("sensefile.dat", "w")

#write the header line in the logging file
timestamp = time.asctime(time.localtime(time.time()))       #timestamp
header = timestamp+","+str(rate)+","+str(samples)+"\n"
sensefile.write(header)


#main loop
for i in range(samples):
    timestamp = time.asctime(time.localtime(time.time()))           #timestamp   
    t = round(sense.get_temperature_from_humidity(),1)              #temperature
    p = round(sense.get_pressure(),1)                               #pressure
    h = round(sense.get_humidity(),1)                               #humidity
    tcpu = cpu_temp()
    t = round((t-(tcpu-t)),1)
    #determine color for progress display
    if t <= 15:
        tcolor = v
    elif (t>15) and (t<=21):
        tcolor = g
    else:
        tcolor = r
    #create the log line for the file
    t = str(t)
    p = str(p)
    h = str(h)
    logline = timestamp+","+t+","+p+","+h+"\n"
    progress = int((i/float(samples)*10))
    sense.show_letter(str(progress), text_colour=tcolor)
    sensefile.write(logline)
    time.sleep(rate)

sensefile.flush()       #commit data to the file
sensefile.close()       #close the sampling file

sense.show_message("Finished")
sense.clear()           #clear SensorHat led display
