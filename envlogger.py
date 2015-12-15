#Environment variables logger
#Program: envlogger.py
#Version 2.6
#Author: Stein Castillo
#Date: Nov 22 2015

#this program reads the environment variables: temperature, pressure and humidity
#the results are logged to the sensefile.dat file.
#on the screen, the program will show the logged values
#at the end, average, maximum and minimum values will presented on the screen

import time
import os
import os.path
import smtplib
email = smtplib.SMTP("smtp.gmail.com", 587)
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

#this function is used to the get the input from the user and validate the data
def get_input(prompt, accepted):
    while True:
        value = input(prompt)
        if value in accepted:
            return(value)
        else:
            print("Invalid input, please try again")
            
#this function is used to read the cpu temperature
def cpu_temp():
    tx = os.popen('/opt/vc/bin/vcgencmd measure_temp')
    cputemp = tx.read()
    cputemp = cputemp.replace('temp=','')
    cputemp = cputemp.replace('\'C\n','')
    cputemp = float(cputemp)
    return cputemp

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

#This functions sens an emai. It is used to notify the user that the sampling process is complete    
def sendemail(toAdd, subject, body):
    smtpUser = "email"
    smtpPass = "password"
    fromAdd = smtpUser
    header = "To: " + toAdd + "\n" + "From: " + fromAdd + "\n" + "Subject: " + subject

    email.ehlo()
    email.starttls()
    email.ehlo()
    email.login(smtpUser, smtpPass)
    email.sendmail(fromAdd, toAdd, header + "\n\n" + body)
    email.quit()
    return()




print("\n")
print("*****************************************")
print("*   Environment Variables Logger        *")
print("*                                       *")
print("*           Version: 2.6                *")
print("*****************************************")
print("\n")

#Check if the log file already exists
filename = "sensefile.dat"
if os.path.isfile(filename):
    rewrite = get_input("Logging file already exists! [R]eplace old, [C]reate new or [Q]uit [R/C/Q]:", ["r", "R", "c", "C", "q", "Q"])
    if str.capitalize(rewrite) == "Q":
        print("Quiting...\n")
        sense.clear()
        exit(0)
    elif str.capitalize(rewrite) == "C":
        senselist = os.popen("ls -l sense*")
        filecount = 0
        while True:
            line = senselist.readline()
            if line == "":
                break
            filecount += 1
        filename = "sensefile"+str(filecount)+".dat"
        print ("Creating new file:", filename)
    elif str.capitalize(rewrite) == "R":
        print ("Replacing sensefile.dat")
        os.popen("rm sensefile.dat")
        
        
#get number of samples and sampling rate from the user
rate = int(input("Enter sample fecuency in seconds:"))
samples = int(input("Enter number of samples:"))

#initialization read from the sensor. This is neccesary since sometimes the sensors return
#a 0 value for pressure on the first read
t = round(sense.get_temperature_from_humidity(),1)            
p = round(sense.get_pressure(),1)                              
h = round(sense.get_humidity(),1)
sense.show_letter("W")
time.sleep(5)
sense.clear()


#these variables will be used to calculate the averages/max/min at the end of the sampling
tt = float(0)
tp = float(0)
th = float(0)
tmax = float(0)
pmax = float(0)
hmax = float(0)
tmin = round(sense.get_temperature_from_humidity(),1)
pmin = round(sense.get_pressure(),1)
hmin = round(sense.get_humidity(),1)

sensefile = open(filename, "w")  #open the sampling file

#write the header line in the logging file
timestamp = time.asctime(time.localtime(time.time()))           #timestamp
header = timestamp+","+str(rate)+","+str(samples)+"\n"
sensefile.write(header)


#print titles
print("Sample".rjust(2), "Temperature".rjust(2), "Pressure".rjust(5), "Humidity".rjust(2), "Time".rjust(6))

#main loop
for i in range(samples):
    timestamp = time.asctime(time.localtime(time.time()))           #timestamp   
    t = round(sense.get_temperature_from_humidity(),1)              #temperature
    p = round(sense.get_pressure(),1)                               #pressure
    h = round(sense.get_humidity(),1)                               #humidity
    tcpu = cpu_temp()
    t = round((t-(tcpu-t)), 1)
    tt = tt + t
    tp = tp + p
    th = th + h
    #determine max/min readings
    tmax = max(tmax, t)
    tmin = min(tmin, t)
    pmax = max(pmax, p)
    pmin = min(pmin, p)
    hmax = max(hmax, h)
    hmin = min(hmin, h)
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
    print (repr(i).rjust(3), t.rjust(11), p.rjust(10), h.rjust(7), timestamp[10:19].rjust(10))
    time.sleep(rate)

sensefile.flush()       #commit data to the file
sensefile.close()       #close the sampling file

#calculate averages
tavg = round(tt/samples, 1)
pavg = round(tp/samples, 1)
havg = round(th/samples, 1)



#convert temperatures to Farenheit
tminf = round(tconv(celsius = tmin), 1)
tmaxf = round(tconv(celsius = tmax), 1)
tavgf = round(tconv(celsius = tavg), 1)

#convert pressure to kPa
pavgk = round(pconv(mb=pavg), 1)
pmaxk = round(pconv(mb=pmax), 1)
pmink = round(pconv(mb=pmin), 1)

#print results
print ("\n")
print ("------------------------------------------------")
print ("Reading", "Temperature".rjust(13), "Pressure".rjust(13), "Humidity".rjust(12))
print ("[*C / *F]".rjust(20), "[mb / Kpa]".rjust(15), "[%]".rjust(8))
print ("------------------------------------------------")
print ("Average", repr(tavg).rjust(6), "/", repr(tavgf), repr(pavg).rjust(8), "/", repr(pavgk), repr(havg).rjust(8))
print ("Maximum", repr(tmax).rjust(6), "/", repr(tmaxf), repr(pmax).rjust(8), "/", repr(pmaxk), repr(hmax).rjust(8))
print ("Minimum", repr(tmin).rjust(6), "/", repr(tminf), repr(pmin).rjust(8), "/", repr(pmink), repr(hmin).rjust(8))
print ("------------------------------------------------")
print ("Number of samples", samples)
print ("\n")


##print ("---------------Averages:---------------------")
##print (repr(tt).rjust(15), repr(tp).rjust(10), repr(th).rjust(7))
##print ("----------------Maximum:---------------------")
##print (repr(maxt).rjust(15), repr(maxp).rjust(10), repr(maxh).rjust(7))
##print ("----------------Minimum:---------------------")
##print (repr(mint).rjust(15), repr(minp).rjust(10), repr(minh).rjust(7))


#send email to nofity process completing
timestamp = time.asctime(time.localtime(time.time()))
mailrecipient = "recipient"
mailsubject = "Sampling process completed!"
mailbody = "Envlogger process successfully completed at " + timestamp + "\n\n" + \
           "A total of " + str(samples) + " samples were taken with a frecuency of " + \
           str(rate) + " seconds"
sendemail(mailrecipient, mailsubject, mailbody)


print ("Finished")
sense.show_message("operation complete")
sense.clear()           #clear SensorHat led display
