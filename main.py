
from utils import *



def display_channel_stats(resp):
	
	for i in resp:
		if(type(resp[i]) is dict):
			print(i+":")
			display_channel_stats(resp[i])
		else:
			print(f"{i}: {resp[i]} \n")

while(True):

	username = input("Search for a YouTube channel's stats \n Type exit to exit search \n Enter username: ")
	if(username == 'exit'):
		break

	
	request = channels_request(part='statistics', forUsername=username)

	response = request.execute()

	try: 
		print("Channel name: "+username+"\n")
		channel = response["items"][0]	#this refers to a specific channel searched.
		display_channel_stats(channel)
	except KeyError:
		print("Channel name not found")
	except:
		print("Another error occured (main.py)")

yt.close()