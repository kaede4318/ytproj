from googleapiclient.discovery import build
from utils import *
import os

#YT_API_KEY = os.environ.get("YT_API_KEY") doesn't work lol


class ProgramError(Exception):
    """Exception indicating an error in the program."""

class InputError(Exception):
    """Exception indicating an error in the program."""


#################
# API Resources #
#################

class Resource:
    """All Resources share same the API key"""
    API_KEY = 'AIzaSyA_GtkfzWH22w_qtB9ACWpBeGsPMPhYgYk' #change key later

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


class PlaylistPage(Resource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resource = self.playlistItems_request()
        self.first = self.__dict__['pageToken']
        self.next = self.get_next_page_token()
        self.vid_ids = self.get_vid_ids()


    def playlistItems_request(self):
        query = {key: value for (key, value) in self.__dict__.items() if key != 'resource'}
        request = Resource.yt.playlistItems().list(**query)
        return request.execute()
        
    def get_next_page_token(self):
        try:
            nextPageToken = self.resource['nextPageToken']

        except:
            nextPageToken = None

        return nextPageToken       

    def get_vid_ids(self):
        return [vid['contentDetails']['videoId'] for vid in self.resource['items']]

    def get_length(self):
        return len(self.vid_ids)


class PlaylistItems(PlaylistPage):

    def __init__(self, pl_id):
        """Create a PlaylistItems Resource object"""
        self.pl_id = pl_id
        self.playlist_pages = []
        self.pl_id_list = []

        self.all_pages()
        self.get_vid_id_list()


    def all_pages(self):
        pl = PlaylistPage(part='contentDetails', playlistId=self.pl_id, maxResults=50, pageToken=None)
        self.playlist_pages.append(pl)
        nextToken = pl.next

        while(nextToken is not None):
            new = PlaylistPage(part='contentDetails', playlistId=self.pl_id, maxResults=50, pageToken=nextToken)
            self.playlist_pages.append(new)
            nextToken = new.next

    def get_vid_id_list(self):
        """Generates list of vid_ids for each PlaylistPage object""" 
        lst = []

        for i in self.playlist_pages:
            lst.append(i.get_vid_ids())

        self.pl_id_list = lst

    def conv_to_str(self, lst):
        """Returns a list of vid_id strings."""
        return list(map(lambda x: ','.join(x), lst))
        

    def calc_playlist_duration(self):
        """Returns a timestamp representing the total length of a YouTube playlist."""
        total_seconds = 0
        lst = self.conv_to_str(self.pl_id_list)    
        for i in lst:
            vid_resource = Videos(
                part='contentDetails',
                id=i)

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