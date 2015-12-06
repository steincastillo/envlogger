# Envlogger


ATTENTION!!!
file completion in progress... 

---- Short Description:
Read temperature, barometric pressure and humidity from the raspberry pi sense hat and log the results in a text file

---- What does it do?
Envlogger reads environment variables (temperature, barometric pressure and humidity) in real time from the raspberry pi sense hat and records the results in a log file. As the sampling process progresses, the program will provide feedback using the sense hat 8x8 led display

The program will give the user control over the sampling frequency and number of samples. 

Also, a program to analyze the log files is included as part of this project.

---- What do you need?
Raspberry pi
sense hat (more info: https://www.raspberrypi.org/learning/getting-started-with-the-sense-hat/)

---- included files:
envlogger.py: "interactive" version of the logging program
envlogger_a.py: "standalone" version of the logging program
logread.py: program to analyze envlogger log files
sensefile.dat: sample data file (optional)
sensefile1.dat: sample data file (60 samples taken every 60 seconds)

--- how does it work?
envlogger.py (interactive version)
open the program on the python idle terminal
execute the program (F5)
Answer the prompts
Voila!
The logging results will be saved to the sensefile.dat

envlogger_a.py (stand alone version)
this version of the program is intended to be executed automatically at startup. This allows for the device to be placed in any location, power up and start the logging process. To do this, the logging parameters have to be setup in the code. These parameters are setup as follows:
look for the section with the comment: #set the samples and sampling rate
rate = sampling frequency in seconds
samples = number of samples
stabilization = [true/false]. Use True to allow for a waiting time to ensure the thermometer adapts to a sudden change of temperature. Use this if you move the device from one room to another. Otherwise, set to False.

logread.py
This program will read a data file created with envlogger (stand alone or interactive) and will display the results of the logging process. At the end, will show a summary of the data including Maximum, Minimum and Average reading for all the variables.

Also will show the temperature readings in celsius (*C) and farenheit (*F) and the pressure reading in milibars (mb) and kilopascals (kPa)

---- 8x8 display messages:
"W": (W)aiting. The program is waiting to stabilize the temperature reading. Useful when the sensor is quickly relocated from one location to another with significat temperature variation. This ensures that max/min/avg calculations will not be distorted by this effect.
"0".."9": Sampling progress. 0=0%, 1=10%, 2=20%, 3=30%, etc.
"Finished": Sampling process complete - standalone mode.
"operation complete": Sampling process complete - interactive mode.



