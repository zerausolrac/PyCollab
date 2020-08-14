
"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Created on May 25, 2016

@author: shurrey

"""

import json
import requests
import time
import jwt
import datetime
import ssl
import sys


class SessionController():

    def __init__(self, target_url, token, verify_certs):
        self.target_url = target_url
        self.token = token
        self.verify_certs = verify_certs

    def getSessionId(self):
        return self.SESSION_ID
    
    def getGuestUrl(self):
        return self.GUEST_URL
    
    def getModUrl(self):
        return self.MODERATOR_URL

    def createSession(self, payload):
        
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        
        r = requests.post("https://" + self.target_url + '/sessions', headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json=payload, verify=self.verify_certs)
        
        if r.status_code == 200:
            res = json.loads(r.text)
            print("Session: " + json.dumps(res,indent=4, separators=(',', ': ')))
            self.SESSION_ID = res['id']
            return(self.SESSION_ID)
        else:
            print("Sessions.createSession ERROR: " + str(r))
            return(None)

    def enrollUser(self, session_id, user, role):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        
        payload = {
            'launchingRole' : role,
            'editingPermission':'writer',
            'user': user
        }
        
        r = requests.post("https://" + self.target_url + '/sessions/' + session_id + "/url", headers={'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json'}, json=payload, verify=self.verify_certs)
        
        if r.status_code == 200:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
            url = res['url']
            return(url)
        else:
            print("Sessions.enrollUser ERROR: " + str(r))
            return(None)


    def get_recordings(self,uuid,start_time):

        endpoint = "https://" + self.target_url + '/recordings?contextExtId=' + uuid + "&startTime=" + str(start_time)
        print("Endpoint: " + endpoint)
        # "Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token

        r = requests.get(endpoint,
                         headers={'Authorization': authStr, 'Content-Type': 'application/json',
                                  'Accept': 'application/json'}, verify=self.verify_certs)
        if r.status_code == 200:
            res = json.loads(r.text)
            return res
        else:
            print(r)

    def get_recording_data(self,recording_id):

                # "Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        url = 'https://' + self.target_url + '/recordings/' + recording_id + '/data'
        r = requests.get(url,
                         headers={'Authorization': authStr, 'Content-Type': 'application/json',
                                  'Accept': 'application/json'}, verify=self.verify_certs)

        if r.status_code == 200:
            res = json.loads(r.text)
            return res
        else:
            print(r)

