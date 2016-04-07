#!usr/bin/python
import os
import sys
import json
from pubnub import Pubnub
from twilio.rest import TwilioRestClient
import time

# Pubnub publish and subscribe keys

send_to_numbers=["+6 ","+61 "]

pubnub = Pubnub(publish_key="key", subscribe_key="key") 

#Extract the Twilio Credentials stored in Bluemix.

if 'VCAP_SERVICES' in os.environ:

    twilioinfo = json.loads(os.environ['VCAP_SERVICES'])['user-provided'][0] 
    twiliocred = twilioinfo["credentials"]
    twilioauthtoken = twiliocred['authToken']
    twilioaccountsid = twiliocred['accountSID']  


def callback(message, channel):
	#input message from IoT device contains the following {"text":"Enter Message Here"} {"phonedestination": "+61111111111","message": "input message goes here"}
	print('this is the message from callback')
	print(message)
	smsmessage = str(message['message'])
	n=0
	for n in range(len(send_to_numbers)):
	 	tophonenumber = send_to_numbers[n]
		
		print smsmessage
		client = TwilioRestClient(twilioaccountsid, twilioauthtoken)
		message = client.sms.messages.create(to=tophonenumber,
	                                     from_="+number",
	                                     body=smsmessage)
		print 'message sent'
	
def error(message):
    print("ERROR : " + str(message))

def connect(message):
	print("CONNECTED")
	
def reconnect(message):
    print("RECONNECTED")

def disconnect(message):
    print("DISCONNECTED")
 
 # main function
if __name__ == "__main__":	
	pubnub.subscribe(channels='hello_world', callback=callback,error=callback,
    	connect=connect, reconnect=reconnect, disconnect=disconnect)