from googleapiclient.discovery import build

def timer():
	start_time = time.time()
	main()
	result = (time.time() - start_time)
	print(f"--- Time elapsed: {result} seconds ---")


def get_vid_length(vid):
	"""get_vid_length takes in a dictionary and returns a string representing the video playtime 
	unformated video length: PT##H##M##S (playtime x hours, x minutes, x seconds)"""
	return vid['contentDetails']['duration']


def get_vid_id(vid):
	"""get_vid_id takes in a dictionary and returns a string representing the video ID (same ID shown in yt url)"""
	return vid['contentDetails']['videoId']


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


################
# API Requests #
################

api_key = 'AIzaSyA_GtkfzWH22w_qtB9ACWpBeGsPMPhYgYk'

yt = build('youtube', 'v3', developerKey=api_key)

def channels_request(**kwargs):
	"""**kwargs are the arguments for list()"""
	return yt.channels().list(**kwargs)


def playlistItems_request(**kwargs):
	"""**kwargs are the arguments for list()"""
	return yt.playlistItems().list(**kwargs)


def videos_request(**kwargs):
	"""**kwargs are the arguments for list()"""
	return yt.videos().list(**kwargs)


yt.close()


