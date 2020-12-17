'''
@ Carlos Suarez
'''
import requests
import base64
import json
from cachetools import TTLCache
import sys
import datetime
import jwt

class AuthControlador():
    path = "/learn/api/public/v1/oauth2/token"
    
    def __init__(self,domain,key,secret):

        self.domain = domain
        self.key = key
        self.secret = secret
        self.cache = None

    def getKey(self):
        return self.key

    def getSecret(self):
        return self.secret


    def setToken(self):
        baseURL = 'https://' + self.domain + self.path
        baseCredencial  = self.key + ':' + self.secret
        credencial = 'Basic ' + str(base64.b64encode(baseCredencial.encode("utf-8")),encoding='utf-8')
        cabecera = {'Authorization': credencial, 'Content-Type':'application/x-www-form-urlencoded'}
        body = 'grant_type=client_credentials' 

        if self.cache != None:
            try:
                token = self.cache['token']
                return token
            except KeyError:
                pass
            except TypeError:
                pass
        try:
            r = requests.post(baseURL,headers=cabecera,data=body)
        except requests.exceptions.RequestException:
            raise Exception('Failed to connect to %s' % baseURL) from None
        if r.status_code == 200:
            parsed_json = json.loads(r.text)
            self.cache = TTLCache(maxsize=1, ttl=parsed_json['expires_in'])
            self.cache['token'] = parsed_json['access_token']
        elif r.status_code == 401:
            print("Your Blackboard Learn credentials are not valid!")
        elif r.status_code == 400:
            print("Your json Config.py is not valid")
        else:
            print("[auth:setToken()] ERROR: " + str(r))


    def getToken(self):
         try:
             if self.cache != None:
                token = self.cache['token']
                return token
             else:
                sys.exit()
         except KeyError:
             self.setToken()
    
             return self.cache['token']
         except TypeError:
             self.setToken()
    
             return self.cache['token']


   
   


