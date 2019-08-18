import time
import astral
import datetime
from datetime import date #Sloppy using but IDC for a little script like this
from vesync.api import VesyncApi

def GetNextStartTime(StrtDate = date.today()):
	#Function Docs = https://astral.readthedocs.io/en/stable/index.html#sun
	#Site to find Elevation = https://www.whatismyelevation.com/
	#Site to find current coordinates = https://www.maps.ie/coordinates.html
	#Location Params = 1 City Name | 2 Country | 3 Latitude | 4 Longitude | 5 Time Zone | 6 Elevation (in meters?)
	loc = astral.Location(('Colorado Springs', 'United States', 38.88, -104.8, 'America/Denver', 1931))

	#Get the sun details from our current location and the date to get details about
	sunEvents = loc.sun(StrtDate)

	#Time before dusk to turn on lights
	duskOffSet = datetime.timedelta(minutes=30)

	#Show user when dusk will be and when the lights will turn on next
	print("Dusk will be at: "+str(sunEvents['dusk']))
	print("Lights will on at: "+str(sunEvents['dusk']-duskOffSet ))

	#Return the date and time to start
	return (sunEvents['dusk']-duskOffSet).replace(tzinfo=None)



def TriggerLights():
	#Custom console colors
	TGREEN =  '\033[32m' # Green Text
	TWHITE = '\033[37m'

	#Sign into API
	api = VesyncApi("USER","PASSWORD")
	
	#For all of the devices
	for i in api.get_devices():	
		#If the device name contains {DS} then it should be controlled by this script
		if('{DS}' in i['deviceName']):
			#Notify user of turning on action
			print(TGREEN + "Turning on | " + i['deviceName'] + " | " + i['cid'] + TWHITE)
			api.turn_on(TGREEN + i['cid'] + TWHITE)



def Main():
	#Start by getting the next time to turn on lights
	NextStartTime = GetNextStartTime()

	#Forever loop
	while True:
		#Get the current time
		now = datetime.datetime.now()
		
		#Check if it is time to turn on the lgiths
		if(now >= NextStartTime):
			#It is time to turn on the lights, notift user and turn lights on
			print("\t\tSTARTING TRIGGER!\n")
			TriggerLights();
			print("\nLIGHTS ON!\n")
			
			#Generate next starting time
			NextStartTime = GetNextStartTime(datetime.datetime.now() + datetime.timedelta(days=1))			
			
			#Extra bit of info to show user the next start time
			print("\nNEXT START ON "+str(NextStartTime)+"\n\n\n")
		else:
			#It was not timr to turn on the lights so show next time on and the current time
			print("NEXT START ON "+str(NextStartTime)+"\t CURRENT TIME "+str(now))
			
			#Wait for 30 seconds before checking again. 
			time.sleep(30)


#Start program
Main()
