from googleapiclient.discovery import build
from utils import *


class ProgramError(Exception):
    """Exception indicating an error in the program."""

class InputError(Exception):
    """Exception indicating an error in the program."""


#################
# API Resources #
#################

class Resource:
    """All Resources share same the API key"""
    API_KEY = 'AIzaSyA_GtkfzWH22w_qtB9ACWpBeGsPMPhYgYk'

    yt = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, **kwargs):
        """Create a default Resource object"""
        self.__dict__.update(kwargs)
        self.resource = None

    def end_service(self):
        yt.close()


class Channels(Resource):

    def __init__(self, **kwargs):
        """Create a Channels Resource object"""
        super().__init__(**kwargs)
        self.resource = self.channels_request()
        
    def channels_request(self):
        query = {key: value for (key, value) in self.__dict__.items() if key != 'resource'}
        request = Resource.yt.channels().list(**query)
        return request.execute()

    def get_channel_name(self):
        print(self.__dict__['forUsername'])

    """class methods"""


class PlaylistItems(Resource):

    def __init__(self, **kwargs):
        """Create a PlaylistItems Resource object"""
        super().__init__(**kwargs)
        self.resource = self.playlistItems_request()
        self.video_ids = self.get_vid_id_list()
        
        #if(len(self.video_ids) == 0):
        #    raise InputError("playlist cannot be empty")

    def playlistItems_request(self):
        query = {key: value for (key, value) in self.__dict__.items() if key != 'resource'}
        request = Resource.yt.playlistItems().list(**query)
        return request.execute()
        
    def get_vid_id(self, vid):
        """get_vid_id takes in a dictionary and returns a string representing the video ID (same ID shown in yt url)"""
        return vid['contentDetails']['videoId']

    def get_vid_ids(self):
        return [self.get_vid_id(vid) for vid in self.resource['items']]

    def get_vid_id_list(self):
        """Returns a timestamp representing the total length of a YouTube playlist."""
        nextPageToken = None
        original_object = self.__dict__
        
        lst = []

        while True:

            lst.extend(self.get_vid_ids())

            try:
                nextPageToken = self.resource['nextPageToken'] 
            except:
                nextPageToken = None

            if not nextPageToken: #breaks if next page doesn't exist
                break
       
            newObj = PlaylistItems(
                part='contentDetails',
                playlistId=original_object['playlistId'],
                maxResults=50,
                pageToken=nextPageToken)

            self.__dict__.update(newObj.__dict__)

        self.__dict__.update(original_object) #reset to original

        return lst


    def calc_playlist_duration(self):
        """Returns a timestamp representing the total length of a YouTube playlist."""
        #Need fix, video request to API cannot be larger than 50 videos at a time. Break the list into chunks?
        total_seconds = 0    
        print("DEBUG: ",len(self.video_ids))
        vid_id_lst_str = ','.join(self.video_ids)

        vid_resource = Videos(
            part='contentDetails',
            id=vid_id_lst_str)

        total_seconds += total_seconds_iso(vid_resource.resource['items'])

        return timestamp(total_seconds)

    """
    def find_playlist_owner(id):
        Finds the owner of the playlist, returns a string, raises error if playlist is empty

        Currently, a bug in the API exists such that a collaborative playlist doesn't differentiate
        who added videos, the API will always return the playlist owner. Thus the else clause will not run

        nextPageToken = None

        pl_request = playlistItems_request(part='snippet', playlistId=id, maxResults=50, pageToken=nextPageToken)

        pl_response = pl_request.execute()

        lst = [pl_response['items'][n]['snippet'].get('channelTitle') for n in range(len(pl_response['items']))]

        if(len(set(lst)) == 0):
            raise ProgramError("Cannot have empty playlist")

        elif(len(set(lst)) == 1):
            return lst[0]

        else:
            return "Multiple authors"
    """



class Videos(Resource):

    def __init__(self, **kwargs):
        """Create a Channels Resource object"""
        super().__init__(**kwargs)
        self.resource = self.videos_request()
       
    def videos_request(self):
        query = {key: value for (key, value) in self.__dict__.items() if key != 'resource'}
        request = Resource.yt.videos().list(**query)
        return request.execute()

    def get_vid_length(vid):
        #get_vid_length takes in a dictionary and returns a string representing the video playtime 
        #unformated video length: PT##H##M##S (playtime x hours, x minutes, x seconds)
        return vid['contentDetails']['duration']



    








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