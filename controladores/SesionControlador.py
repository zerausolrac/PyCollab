'''
@ Carlos Suarez 2020
'''

import requests
import datetime
import time 
import json
from cachetools import TTLCache
import ssl
import sys

class SesionControlador():
    def __init__(self,url,token,cert):
        self.url = url
        self.token = token
        self.cert = cert

    def getGrabaciones(self,cursoUUID,tiempo):
        endpoint = 'https://' + self.url + '/recordings' + "?contextExtId=" + cursoUUID + "&startTime=" + str(tiempo)
        bearer = "Bearer " + self.token
        rheaders = {
            "Authorization":bearer,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.get(endpoint,headers=rheaders,verify=self.cert)
        if r.status_code == 200:
            res = json.loads(r.text)
            return res
        else:
            print(r)
    
    def get_recording_data(self,recording_id):

                # "Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        url = 'https://' + self.url + '/recordings/' + recording_id + '/data'
        r = requests.get(url,
                         headers={'Authorization': authStr, 'Content-Type': 'application/json',
                                  'Accept': 'application/json'}, verify=self.cert)

        if r.status_code == 200:
            res = json.loads(r.text)
            return res
        else:
            print(r)


    