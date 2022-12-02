import isodate
import re
import time
from googleapiclient.discovery import build
from datetime import timedelta

api_key = 'AIzaSyA_GtkfzWH22w_qtB9ACWpBeGsPMPhYgYk'

ex_pl = 'PL7h7m34DLvE8LTyVZTilk2l6Yaf9Td17q'
ex_pl2 = 'PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU'
ex_channel_id = 'UCEG2_W5OLFrU6qUfGVgIraA'

#calculates the total length in seconds using regular expressions, returns seconds as an int
def total_seconds_re(vid_list):
	hours_pattern = re.compile(r'(\d+)H')
	minutes_pattern = re.compile(r'(\d+)M')
	seconds_pattern = re.compile(r'(\d+)S')

	pl_total_seconds = 0

	for vid in vid_list:
		duration = vid['contentDetails']['duration']

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
		iso_8601_duration = vid['contentDetails']['duration'] #unformated video length: PT##H##M##S (playtime x hours, x minutes, x seconds)
		dt = isodate.parse_duration(iso_8601_duration)
		vid_total_seconds = dt.total_seconds() #video length in seconds (int)

		pl_total_seconds += vid_total_seconds

	return int(pl_total_seconds)

#changes yt format PT##H##M##S to HH:MM:SS (string)
def format_yt_vid_length(total_seconds):
	minutes, seconds = divmod(total_seconds, 60)
	hours, minutes = divmod(minutes, 60)

	#format: maybe replace later
	if(seconds//10 == 0):
		seconds = "0"+str(seconds)
	if(minutes//10 == 0):
		minutes = "0"+str(minutes)

	return f'{hours}:{minutes}:{seconds}'

def main():
	yt = build('youtube', 'v3', developerKey=api_key)

	total_seconds = 0

	nextPageToken = None
	while True:
		pl_request = yt.playlistItems().list(
				part='contentDetails',
				playlistId=ex_pl2,
				maxResults=50,
				pageToken=nextPageToken

			)

		pl_response = pl_request.execute()

		vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]
		"""
		vid_ids = []
		for item in pl_response['items']:
			vid_ids.append(item['contentDetails']['videoId'])
		"""

		vid_request = yt.videos().list(
				part='contentDetails',
				id=','.join(vid_ids)

			)

		vid_response = vid_request.execute()

		total_seconds += total_seconds_iso(vid_response['items'])

		nextPageToken = pl_response.get('nextPageToken')

		if not nextPageToken:
			break

	print(total_seconds, format_yt_vid_length(total_seconds))

	yt.close()

'''
def timer():
	start_time = time.time()
	main()
	result = (time.time() - start_time)
	print(f"--- Time elapsed: {result} seconds ---")

timer()
'''
if __name__ == "__main__":
	main()
