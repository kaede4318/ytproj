import isodate
import re
import time

from googleapiclient.discovery import build
from datetime import timedelta
from utils import *
from classes import *



#calculates the total length in seconds using regular expressions, returns seconds as an int
def total_seconds_re(vid_list):
	hours_pattern = re.compile(r'(\d+)H')
	minutes_pattern = re.compile(r'(\d+)M')
	seconds_pattern = re.compile(r'(\d+)S')

	pl_total_seconds = 0

	for vid in vid_list:
		duration = get_vid_length(vid)

		hours = hours_pattern.search(duration)
		minutes = minutes_pattern.search(duration)
		seconds = seconds_pattern.search(duration)

		hours = int(hours.group(1)) if hours else 0
		minutes = int(minutes.group(1)) if minutes else 0
		seconds = int(seconds.group(1)) if seconds else 0

		video_seconds = timedelta(
			hours=hours,
			minutes=minutes,
			seconds=seconds
		).total_seconds()

		pl_total_seconds += video_seconds

	return int(pl_total_seconds)


#calculates the total length in seconds using isodate utility functions, returns seconds as an int
def total_seconds_iso(vid_list):
	pl_total_seconds = 0

	for vid in vid_list:
		iso_8601_duration = get_vid_length(vid) 
		dt = isodate.parse_duration(iso_8601_duration)
		vid_total_seconds = dt.total_seconds() #video length in seconds (int)

		pl_total_seconds += vid_total_seconds

	return int(pl_total_seconds)


def calc_playlist_duration(id):

	total_seconds = 0

	nextPageToken = None
	while True:
		pl_request = playlistItems_request(part='contentDetails', playlistId=id, maxResults=50, pageToken=nextPageToken)

		pl_response = pl_request.execute()


		vid_ids = [get_vid_id(vid) for vid in pl_response['items']]
		"""
		vid_ids = []
		for item in pl_response['items']:
			vid_ids.append(item['contentDetails']['videoId'])
		"""
		vid_list_str = ','.join(vid_ids)
		vid_request = videos_request(part='contentDetails', id=vid_list_str)

		vid_response = vid_request.execute()

		total_seconds += total_seconds_iso(vid_response['items'])

		nextPageToken = pl_response.get('nextPageToken')

		if not nextPageToken: #breaks if next page does not exist
			break

	return timestamp(total_seconds)


def find_playlist_owner(id):
	"""Finds the owner of the playlist
	"""

	nextPageToken = None

	pl_request = playlistItems_request(part='snippet', playlistId=id, maxResults=50, pageToken=nextPageToken)

	pl_response = pl_request.execute()

	lst = [pl_response['items'][n]['snippet'].get('channelTitle') for n in range(len(pl_response['items']))]

	if(len(set(lst)) == 0):
		raise ProgramError("Cannot have empty playlist")

	elif(len(set(lst)) == 1):
		return pl_response['items'][0]['snippet'].get('channelTitle')

	else:
		return "Multiple authors"
