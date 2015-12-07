#analyse files created with the envlogger program 
#Program: logread.py 
#Version 1.5 
#Author: Stein Castillo 
#Date: Nov 30 2015 
#---------------------- 

import os 
#os.chdir("/home/pi/stein/projects/python")  #set the working directory 
 
 #this function is used to convert temperature readings Celsius<->Farenheit 
def tconv (celsius=0, farenheit=0): 
     if farenheit == 0: 
         conv = (celsius*1.8)+32 
     elif celsius == 0: 
         conv = (farenheit - 32)/1.8 
     else: 
         conv = 0 
     return (conv) 
 
 #this function is used to convert preasure readings milibars(mb)<->Kilopascal(KPa) 
def pconv (mb = 0, kpa = 0): 
     if mb == 0: 
         conv = kpa * 10 
     elif kpa == 0: 
         conv = mb * 0.1 
     else: 
         conv = 0 
     return (conv) 
 
#  computeHeight() - the conversion uses the formula: 
# 
#  h = (T0 / L0) * ((p / P0)**(-(R* * L0) / (g0 * M)) - 1) 
# 
#  where: 
#  h  = height above sea level 
#  T0 = standard temperature at sea level = 288.15 
#  L0 = standard temperatur elapse rate = -0.0065 
#  p  = measured pressure 
#  P0 = static pressure = 1013.25 
#  g0 = gravitational acceleration = 9.80665 
#  M  = mloecular mass of earth's air = 0.0289644 
#  R* = universal gas constant = 8.31432 
# 
#  Given the constants, this works out to: 
# 
#  h = 44330.8 * (1 - (p / P0)**0.190263) 
def computeHeight(pressure): 
    return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263)) 

#initialize variables 
#(t)emperature, (p)ressure, (h)humidity     
tmin = 100 
pmin = 1000 
hmin = 100 
#- 
tmax = 0 
pmax = 0 
hmax = 0 
#- 
tsum = 0 
psum = 0 
hsum = 0 
index = 0 

 
print("\n") 
print("*****************************************") 
print("*   Environment Log File Analyzer       *") 
print("*                                       *") 
print("*           Version: 1.5                *") 
print("*****************************************") 
print("\n") 

name = input("file name:")                  #get the file to analyze 

#Check if the log file already exists 
if not(os.path.isfile(name)): 
    print ("Files does not exist... cancelling.") 
    exit(0) 


dump = input("Log file screen dump [y/n]:") 
dump = str.capitalize(dump) 

#open log file, read only 
logfile = open(name, "r") 

print ("Analysing flile...") 

#read file header 
header = logfile.readline() 
header = header.split(",") 
hsample = float(header[2]) 

#main loop 
for line in logfile: 
    logline = line.strip() 
    if dump == "Y": 
        print (logline) 
    logline = logline.split(",")  #convert the read line to a list using "," as separator 
    d = logline[0]              #extract the date 
    t = float(logline[1])       #extract the temperature 
    p = float(logline[2])       #extract the pressure 
    h = float(logline[3])       #extract the humidity 
    #calculate max and min reading 
    tmin = min(tmin, t) 
    pmin = min(pmin, p) 
    hmin = min(hmin, h) 
    tmax = max(tmax, t) 
    pmax = max(pmax, p) 
    hmax = max(hmax, h) 
    tsum = tsum + t 
    psum = psum + p 
    hsum = hsum + h 
    index = index + 1 
     
logfile.close()                 #close the file 
print ("Complete...") 

#calculate averages 
tavg = round((tsum/index), 1) 
pavg = round((psum/index), 1) 
havg = round((hsum/index), 1) 

#convert temperatures to Farenheit 
tminf = round(tconv(celsius = tmin), 1) 
tmaxf = round(tconv(celsius = tmax), 1) 
tavgf = round(tconv(celsius = tavg), 1) 

#convert pressure to kPa 
pavgk = round(pconv(mb=pavg), 1) 
pmaxk = round(pconv(mb=pmax), 1) 
pmink = round(pconv(mb=pmin), 1) 

#Calculate altitude 
altitude = round(computeHeight(pavg), 1) 

 
#print results 
print ("\n") 
print ("------------------------------------------------") 
print ("| Sampling parameters:                         |") 
print ("------------------------------------------------") 
print ("Date:", header[0]) 
print ("Frecuency (seconds):", header[1]) 
print ("Samples:", int(hsample)) 
print ("------------------------------------------------") 
print ("Reading", "Temperature".rjust(13), "Pressure".rjust(13), "Humidity".rjust(12)) 
print ("[*C / *F]".rjust(20), "[mb / Kpa]".rjust(15), "[%]".rjust(8)) 
print ("------------------------------------------------") 
print ("Average", repr(tavg).rjust(6), "/", repr(tavgf), repr(pavg).rjust(8), "/", repr(pavgk), repr(havg).rjust(8)) 
print ("Maximum", repr(tmax).rjust(6), "/", repr(tmaxf), repr(pmax).rjust(8), "/", repr(pmaxk), repr(hmax).rjust(8)) 
print ("Minimum", repr(tmin).rjust(6), "/", repr(tminf), repr(pmin).rjust(8), "/", repr(pmink), repr(hmin).rjust(8)) 
print ("------------------------------------------------") 
print ("Altitude:", altitude) 
print ("\n") 


#plot results (temperature)
import numpy as np
import matplotlib.pyplot as plt

#extract from the file temperature (col 1) and pressure (Col 2) as an array
logfile = np.loadtxt(name, delimiter=",", usecols=(1,2))
tplot = logfile[1:,0]   #extract temperature from the arrah
del logfile             #delete logfile array 
#set plot parameters
plt.xlabel("Samples")
plt.ylabel("Degrees Celsius")
plt.title("Temperature")
#display the temperature chart
plt.plot(tplot, "-b")
plt.show()