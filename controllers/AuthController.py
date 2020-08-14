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
from cachetools import TTLCache
import requests
import time
import jwt
import datetime
import ssl
import sys

class AuthController():
    target_url = ''
    def __init__(self, url, key, secret, verify_certs):
        
        self.key = key
        self.secret = secret

        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes = 5)

        headers = {
            'typ' : 'JWT',
            'alg': "RS256"     
        }
 
        claims = {
            "iss" : self.key ,
            "sub" : self.key ,
            "exp" : exp 
        }
        
        self.assertion = jwt.encode(claims, self.secret)
        
        self.grant_type = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
        
        self.payload = {
            'grant_type':self.grant_type,
            'assertion' : self.assertion
            
        }
        
        self.target_url = url
        self.verify_certs = verify_certs
  
        self.cache = None

    def getKey(self):
        return self.key

    def getSecret(self):
        return self.secret

    def setToken(self):
        endpoint = 'https://' + self.target_url + '/token'

        if self.cache != None:
            try:
                token = self.cache['token']

                return
            
            except KeyError:

                pass

            except TypeError:

                pass
    
        # Authenticate
        r = requests.post(endpoint, data=self.payload, auth=(self.key, self.secret), verify=self.verify_certs)

        print("[auth:setToken()] STATUS CODE: " + str(r.status_code) )
        #strip quotes from result for better dumps
        res = json.loads(r.text)
        print("[auth:setToken()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))

        if r.status_code == 200:
            parsed_json = json.loads(r.text)
            
            self.cache = TTLCache(maxsize=1, ttl=parsed_json['expires_in'])

            self.cache['token'] = parsed_json['access_token']

        else:
            print("[auth:setToken()] ERROR: " + str(r))

    def getToken(self):
        #if token time is less than a one second then
        # print that we are pausing to clear
        # re-auth and return the new token
        try:
            token = self.cache['token']

            return token
        except KeyError:
            self.setToken()
    
            return self.cache['token']
        except TypeError:
            self.setToken()
    
            return self.cache['token']
