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

    def __repr__(self):
        #lst = [key+'='+str(self.__dict__.get(key)) for key in self.__dict__ if key != 'resource'] #Equivalent to below
        #return 'Resource(' + ', '.join(lst) + ')'
        params = ['{0}={1}'.format(k, v) for k, v in self.__dict__.items() if k != 'resource'] #don't include resource for clarity
        return 'Resource(' + ', '.join(params) + ')'
    
    """__str__"""


class PlaylistPage(Resource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resource = self.playlistItems_request()
        self.vid_ids = self.get_vid_ids()

        self.first = self.__dict__['pageToken']
        self.next = self.get_next_page_token()

        #self.__dict__['playlistId'] PLAYLIST ID

    def __repr__(self):
        params = ['{0}={1}'.format(k, v) for k, v in self.__dict__.items() if k != 'resource'] #don't include resource for clarity
        return 'PlaylistPage(' + ', '.join(params) + ')'

    """__str__"""

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
        """Logic to handle temporary new object created in get_playlist_owner"""
        try: 
            return [vid['contentDetails']['videoId'] for vid in self.resource['items']]
        except:
            return []

    def get_length(self):
        return len(self.vid_ids)

    def get_playlist_owner(self):
        """Finds the owner of the playlist, returns a string, raises error if playlist is empty

        Currently, a bug in the API exists such that a collaborative playlist doesn't differentiate
        who added videos, the API will always return the playlist owner. Thus the else clause will not run"""

        """Create new PlaylistPage object:"""
        pl_request = PlaylistPage(
            part='snippet', 
            playlistId=self.__dict__['playlistId'], 
            maxResults=50, 
            pageToken=self.first)
        
        lst = [pl_request.resource['items'][n]['snippet'].get('channelTitle') for n in range(len(pl_request.resource['items']))]

        return lst


class PlaylistItems(PlaylistPage):

    def __init__(self, pl_id):
        """Create a PlaylistItems Resource object"""
        self.pl_id = pl_id
        self.playlist_pages = []
        self.pl_id_list = []

        self.all_pages()
        self.get_vid_id_list()

    def __repr__(self):
        params = [repr(page) for page in self.playlist_pages] 
        return 'PlaylistItems([' + ', '.join(params) + '])' #maybe change?

        """Or use this definition?
        return 'PlaylistItems(' + self.pl_id + ')'
        """

    """__str__"""

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

    
    def find_playlist_owner(self):
        """Finds the owner of the playlist, returns a string, raises error if playlist is empty

        Currently, a bug in the API exists such that a collaborative playlist doesn't differentiate
        who added videos, the API will always return the playlist owner. Thus the else clause will not run"""
        lst = []

        for i in self.playlist_pages: 
            lst.extend(i.get_playlist_owner())

        if(len(set(lst)) == 0):
            raise ProgramError('Cannot have empty playlist')

        elif(len(set(lst)) == 1):
            return lst[0]

        else:
            return 'Multiple authors: ' + ', '.join(lst)    #authors or owners?
    


class Channels(Resource):

    def __init__(self, **kwargs):
        """Create a Channels Resource object"""
        super().__init__(**kwargs)
        self.resource = self.channels_request()
        
    def __repr__(self):
        params = ['{0}={1}'.format(k, v) for k, v in self.__dict__.items() if k != 'resource'] #don't include resource for clarity
        return 'Channels(' + ', '.join(params) + ')'    

    """__str__"""

    def channels_request(self):
        query = {key: value for (key, value) in self.__dict__.items() if key != 'resource'}
        request = Resource.yt.channels().list(**query)
        return request.execute()

    def get_channel_name(self):
        print(self.__dict__['forUsername'])

    """class methods"""



class Videos(Resource):

    def __init__(self, **kwargs):
        """Create a Channels Resource object"""
        super().__init__(**kwargs)
        self.resource = self.videos_request()
       
    def __repr__(self):
        params = ['{0}={1}'.format(k, v) for k, v in self.__dict__.items() if k != 'resource'] #don't include resource for clarity
        return 'Videos(' + ', '.join(params) + ')'   

    """__str__"""

    def videos_request(self):
        query = {key: value for (key, value) in self.__dict__.items() if key != 'resource'}
        request = Resource.yt.videos().list(**query)
        return request.execute()

    def get_vid_length(vid):
        #get_vid_length takes in a dictionary and returns a string representing the video playtime 
        #unformated video length: PT##H##M##S (playtime x hours, x minutes, x seconds)
        return vid['contentDetails']['duration']


