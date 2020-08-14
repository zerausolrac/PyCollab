
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

class UserController():

    def __init__(self, target_url, token, verify_certs):
        self.target_url = target_url
        self.token = token
        self.verify_certs = verify_certs

    def createUser(self, userJson):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        
        r = requests.post("https://" + self.target_url + '/users', headers={ 'Authorization':authStr,'Content-Type':'application/json','Accept':'application/json' }, json=userJson, verify=self.verify_certs)

        if r.status_code == 200:
            res = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
            userId = res['id']
            return(userId)
        else:
            print("Users.createUser ERROR: " + str(r))
            return(None)