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


def format_yt_vid_length(total_seconds):
	"""changes yt format PT##H##M##S to HH:MM:SS (returns a string)"""
	minutes, seconds = divmod(total_seconds, 60)
	hours, minutes = divmod(minutes, 60)

	#formatting logic: maybe replace later
	if(seconds//10 == 0):
		seconds = "0"+str(seconds)
	if(minutes//10 == 0):
		minutes = "0"+str(minutes)

	return f'{hours}:{minutes}:{seconds}'