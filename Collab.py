'''
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on May 25, 2016

@author: shurrey
'''

import sys
import os
import getopt
import datetime
import uuid
import json
import urllib.request

import argparse
import ntpath # so we can grab the basename off the end of the full-file-path.
import time
import urllib3

# Import Config
import Config




# Import Controllers
from controllers import AuthController
from controllers import UserController
from controllers import SessionController
from controllers import ContextController

# Import Models
from models import User
from models import Session

class Collab():

    def __init__ (self):
        self.URL = Config.adict['collab_base_url']
        self.COLLAB_KEY = Config.adict['collab_key']
        self.COLLAB_SECRET = Config.adict['collab_secret']

        if Config.adict['verify_certs'] == 'True':
            self.COLLAB_CERTS = True
        else:
            self.COLLAB_CERTS = False

        self.authorized_session = None
        
    def getToken(self):
        self.authorized_session = AuthController.AuthController(self.URL, self.COLLAB_KEY, self.COLLAB_SECRET,self.COLLAB_CERTS)
        self.authorized_session.setToken()
        return(self.authorized_session.getToken())
        

    def get_recordings(self, course_uuid, startTime):
        sessions = SessionController.SessionController(self.URL, self.getToken(), self.COLLAB_CERTS)
        recordings = sessions.get_recordings(course_uuid, startTime)
        print (str(recordings))
        return recordings

    def get_recording_data(self,recording_id):
        sessions = SessionController.SessionController(self.URL, self.getToken(), self.COLLAB_CERTS)
        recordingid = sessions.get_recording_data(recording_id)
        print(str(recordingid))
        return recordingid

    def getCourseName(self, course_uuid):
        contexts = ContextController.ContextController(self.URL, self.getToken(), self.COLLAB_CERTS)
        return(contexts.getContext(course_uuid))


#other functions for recordings
#Creating a list for recordings that need to be downloaded
def listrecordings(recordings):
    recordinglist = []
    x=0
    try:
        number_of_recordings = (len(recordings['results']))
        if number_of_recordings <= 0:
            return None
        while x < number_of_recordings:
            recordinglist.append({"recording_id" : recordings['results'][x]['id'], "recording_name" : recordings['results'][x]['name'] })
            x += 1
        print(str(recordinglist))
        return recordinglist
    except TypeError:
        return None

#downloading the recordings

def downloadrecording(recording_list, name, course_uuid):
    for recording in recording_list:
        recording_data = collab_service.get_recording_data(recording['recording_id'])
        print(str(recording_data))
        print('**** Downloading recording with id ****' + recording['recording_id'])
        filename = name + ' - ' + recording['recording_name'].replace(':', ' ').replace('/', ' ').replace('”', '').replace('“', '').replace(',', '').replace('?', '') + '.mp4'
        fullpath = './downloads/'
        print(fullpath + filename)
        urllib.request.urlretrieve(recording_data['extStreams'][0]['streamUrl'], fullpath + filename)
        #upload_creator = UploadAndCreateLink()
        #upload_creator.upload_and_create_link(fullpath + filename, course_uuid)


if __name__ == "__main__":
    collab_service = Collab()
    
    course_uuids = [ 
        'e6dc5e12678a451d861fcffd1ebd901a'
    ]

    start_time = datetime.datetime.now() - datetime.timedelta(weeks=12)
    start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    print(start_time)

    for course_uuid in course_uuids:
        print("uuid: " + course_uuid)
        course_name = collab_service.getCourseName(course_uuid)
        print("name: " + str(course_name))
        sessions_json = collab_service.get_recordings(course_uuid, start_time)
        recording_list= listrecordings(sessions_json)
        if recording_list is None:
            print("No recordings available for course: " + course_name)
        else:
            downloadrecording(recording_list, course_name, course_uuid)



    