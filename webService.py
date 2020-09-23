import requests
import json
import Config
import sys
import datetime
import urllib.request
import time 

from tqdm import tqdm 

from controladores import AuthControlador
from controladores import JotControlador
from controladores import SesionControlador

class WebService():
    
    def __init__(self):
        self.KEY = Config.credenciales['learn_rest_key']
        self.SECRET = Config.credenciales['learn_rest_secret']
        self.DOMAIN = Config.credenciales['learn_rest_fqdn']
        self.KEY_C = Config.credenciales['collab_key']
        self.SECRET_C = Config.credenciales['collab_secret']
        self.DOMAIN_C = Config.credenciales['collab_base_url']
        if Config.credenciales["verify_certs"] == 'True':
            self.CERT = True
        else:
            self.CERT = False

        self.sesion = None
        self.jsesion = None

    def getToken(self):
         self.sesion = AuthControlador.AuthControlador(self.DOMAIN,self.KEY, self.SECRET)
         self.sesion.setToken()
         return(self.sesion.getToken())

    def getJot(self):
        self.jsesion = JotControlador.JotControlador(self.DOMAIN_C,self.KEY_C, self.SECRET_C,self.CERT)
        self.jsesion.setJot()
        return self.jsesion.getJot() 



    def getUser(self, userId):
        self.userId = userId
        userURL =  '/learn/api/public/v1/users/userName:' + userId
        getURL = 'https://' + self.DOMAIN + userURL
        credencial = {'Authorization' : 'Bearer ' + self.getToken()}
        r = requests.get(getURL,headers=credencial)
        print(r)
        
    

    def getUUID(self,course_id):
        self.course_id = course_id
        courseURL = "/learn/api/public/v1/courses/courseId:" + course_id 
        getURL = 'https://' + self.DOMAIN + courseURL
        credencial = {'Authorization' : 'Bearer ' + self.getToken()}
        r = requests.get(getURL,headers=credencial)
        parsed_json = json.loads(r.text)
        return parsed_json['uuid']


    def getGrabaciones(self,cursoUUID,tiempo):
        sesionCollab = SesionControlador.SesionControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        grabaciones = sesionCollab.getGrabaciones(cursoUUID,tiempo)
        return(grabaciones)
    
    def get_recording_data(self,recording_id):
        sessions = SesionControlador.SesionControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        recordingid = sessions.get_recording_data(recording_id)
        #print(str(recordingid))
        return recordingid

    
    

