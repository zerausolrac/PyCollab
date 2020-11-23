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

class MoodleControlador():

    def __init__(self,domain,token,cert):
        self.domain = domain
        self.token = token 
        self.cert = cert 

    #Moodle LTI

    def getGrabacionesMoodleContextoLTI(self,moodle_id,tiempo):
        endpoint = 'https://' + self.domain + '/contexts/?extId=' + moodle_id 
        bearer = "Bearer " + self.token
        headers = {
            "Authorization":bearer,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.get(endpoint,headers=headers,verify=self.cert)
        if r.status_code == 200:
            jsonInfo = json.loads(r.text)
            if jsonInfo['size'] > 0:
                contexto_id = jsonInfo['results'][0]['id']
                return contexto_id
            else:
                return None
        else:
            print("Error Moodle ContextoLTI:" , str(r))




    def grabacionesMoodleLTI(self,contexto_id):
        endpoint = 'https://' + self.domain + '/recordings/?contextId=' + contexto_id 
        bearer = "Bearer " + self.token
        headers = {
            "Authorization":bearer,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.get(endpoint,headers=headers)
        if r.status_code == 200:
            jsonInfo = json.loads(r.text)
            return jsonInfo
        else:
            print("Error GrabacionesLTL: " , str(r))



    def get_moodleLTI_recording_data(self,recording_id):
        authStr = 'Bearer ' + self.token
        url = 'https://' + self.domain + '/recordings/' + recording_id + '/data'
        credencial ={
           'Authorization': authStr,
           'Content-Type': 'application/json',
           'Accept': 'application/json'
        }
        r = requests.get(url,headers=credencial, verify=self.cert)
        if r.status_code == 200:
            res = json.loads(r.text)
            return res
        else:
            print(r)


    #Moodle plugin 

    def moodleSesionName(self,sesionId):
        endpoint = 'https://' + self.domain + '/sessions/'  + sesionId 
        credencial = {
            "Authorization":"Bearer " + self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.get(endpoint,headers=credencial,verify=self.cert)
        if r.status_code == 200:
            res = json.loads(r.text)
            return res['name']
        else:
            print("Error Session:", str(r))




    def listaCompletaSessiones(self,criteria):
        listaFiltrada = []
        endpoint = 'https://' + self.domain + '/sessions' 
        credencial = {
            "Authorization":"Bearer " + self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.get(endpoint,headers=credencial,verify=self.cert)
        if r.status_code == 200:
            res = json.loads(r.text)
            resultado = res['results']
            for sesion in resultado:
                if criteria in sesion['name']:
                   listaFiltrada.append({'id':sesion['id'], 'name':sesion['name']}) 

            return listaFiltrada
        else:
            print("Error Session:", str(r))





    def listaCompletaMoodleGrabaciones(self):
        listaGrabaciones = []
        endpoint = 'https://' + self.domain + '/recordings'
        credencial = {
            'Authorization': 'Bearer ' + self.token,
            'Accept':'application/json'
        }
        r = requests.get(endpoint,headers=credencial,verify=self.cert)
        if r.status_code == 200:
            jsonInfo = json.loads(r.text)
            resultado = jsonInfo['results']
            if len(resultado) == 0:
                print("No recordings found")
            else:
                for grabacion in resultado:
                    listaGrabaciones.append({'id':grabacion['id'], 'name':grabacion['name']})
                print(listaGrabaciones)

        else:
            print("Error listaGrabación Moodle:", str(r))



    def listaMoodleGrabaciones(self,sname):
        endpoint = 'https://' + self.domain + '/recordings?name='  + sname 
        credencial = {
            "Authorization":"Bearer " + self.token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.get(endpoint,headers=credencial,verify=self.cert)
        if r.status_code == 200:
            res = json.loads(r.text)
            idx = 0
            recording_ids = []
            try:
                numero_grabaciones = len(res['results'])
                if numero_grabaciones <= 0:
                    return None
                while idx < numero_grabaciones:
                    if 'storageSize' in res['results'][idx]:
                        recording_ids.append({
                            'recording_id':res['results'][idx]['id'],
                            'recording_name':res['results'][idx]['name'],
                            'duration':res['results'][idx]['duration'],
                            'storageSize':res['results'][idx]['storageSize'],
                            'created':res['results'][idx]['created']
                        })
                    else:
                        recording_ids.append({
                            'recording_id':res['results'][idx]['id'],
                            'recording_name':res['results'][idx]['name'],
                            'duration':res['results'][idx]['duration'],
                            'storageSize':0,
                            'created':res['results'][idx]['created']
                        })
                    idx += 1
                return recording_ids
            except TypeError:
                return None    
        else:
            return None

