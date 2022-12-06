import isodate
import re
import time

from googleapiclient.discovery import build
from datetime import timedelta


def timer():
	start_time = time.time()
	main()
	result = (time.time() - start_time)
	print(f"--- Time elapsed: {result} seconds ---")

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
		iso_8601_duration = vid['contentDetails']['duration'] #get_vid_length(vid) 
		dt = isodate.parse_duration(iso_8601_duration)
		vid_total_seconds = dt.total_seconds() #video length in seconds (int)

		pl_total_seconds += vid_total_seconds

	return int(pl_total_seconds)

def timestamp(total_seconds):
	"""changes seconds integer to HH:MM:SS (returns a string)"""
	minutes, seconds = divmod(total_seconds, 60)
	hours, minutes = divmod(minutes, 60)

	
	#format so single digits have a leading 0
	seconds = f"{seconds:02d}" 
	if(hours == 0):
		return f'{minutes}:{seconds}'

	else:
		minutes = f"{minutes:02d}"
		return f'{hours}:{minutes}:{seconds}'

def get_video_https_link(vid_id):
	return "https://www.youtube.com/playlist?list=" + vid_id

def get_playlist_https_link(pl_id):
	return "https://www.youtube.com/watch?v=" + pl_id




