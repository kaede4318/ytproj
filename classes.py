from googleapiclient.discovery import build



class ProgramError(Exception):
    """Exception indicating an error in the program."""

class Resource:
    """All share same API key"""
    #note count how many times the build gets called and how many times the close called
    api_key = 'AIzaSyA_GtkfzWH22w_qtB9ACWpBeGsPMPhYgYk'

    yt = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Channels(Resource):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def channels_request(self):
        return Resource.yt.channels().list(**self.__dict__)

    """Class functions"""

"""
class PlaylistItems(Resource):

    def __init__(self, **kwargs):
        super().__init__()

    def channels_request():
        return yt.playlistItems().list(self.query)

    
    #ONLY WORKS WITH pl_response
    def get_vid_id(vid):
        get_vid_id takes in a dictionary and returns a string representing the video ID (same ID shown in yt url)
        return vid['contentDetails']['videoId']


class Videos(Resource):

    def __init__(self, **kwargs):
        super().__init__()

    def channels_request():
        return yt.videos().list(self.query)

    Class functions
    def get_vid_length(vid):
        get_vid_length takes in a dictionary and returns a string representing the video playtime 
        unformated video length: PT##H##M##S (playtime x hours, x minutes, x seconds)
        return vid['contentDetails']['duration']
"""