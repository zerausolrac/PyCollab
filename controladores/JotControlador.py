'''
@ Carlos Suarez
'''
import jwt
import requests
import datetime
import time 
import json
from cachetools import TTLCache
import ssl
import sys


class JotControlador():
    
    def __init__(self,domain, key, secret,cert):
        self.domain = domain
        self.key = key
        self.secret = secret 
        self.cert = cert
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=5.0)

       
        header = {
           "alg":"RS256",
           "typ":"JWT"
        }

        claims = {
           "iss": self.key,
           "sub": self.key,
           "exp": exp
        }

        self.assertion = jwt.encode(claims,self.secret)
        self.grant_type = "urn:ietf:params:oauth:grant-type:jwt-bearer"

        self.payload = {
           "grant_type": self.grant_type,
           "assertion": self.assertion
        }

        self.verify_cert = cert
        self.jcache = None


    def getKey(self):
        return self.key

    def getSecret(self):
        return self.secret   
    
    def setJot(self):
       #Crear la petición ocn el header, payload y signature
       endpoint = 'https://' + self.domain + '/token'
       if self.jcache != None:
            try:
               token = self.jcache["jwtoken"]
               return token
            except KeyError: 
               pass
            
        
       r = requests.post(endpoint, data=self.payload, auth=(self.key, self.secret), verify=self.cert)
       if r.status_code == 200:
            json_valores = json.loads(r.text)
            self.jcache = TTLCache(maxsize=1, ttl=json_valores['expires_in'])
            self.jcache['jwtoken'] = json_valores['access_token']
       else:
            print("[auth:jotToken()] ERROR: " + str(r))



    def getJot(self):
      try:
            token = self.jcache['jwtoken']
            return token
      except KeyError:
            self.setJot()
            return self.jcache['jwtoken']   

