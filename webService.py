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

        print("WebService encendido...")
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

    
    
def listaGrabaciones(recordings):

        recordinglist = []
        x=0
        try:
          number_of_recordings = (len(recordings['results']))
          if number_of_recordings <= 0:
             return None
          while x < number_of_recordings:
             recordinglist.append({"recording_id" : recordings['results'][x]['id'], "recording_name" : recordings['results'][x]['name'] })
             x += 1
          #print(str(recordinglist))
          return recordinglist
        except TypeError:
         return None





def descargarGrabacion(url:str, fname:str):
    resp = requests.get(url,stream=True)
    total = int(resp.headers.get('content-length',0))
    progress_bar = tqdm(total=total, unit='iB', unit_scale=True,unit_divisor=1024)
    with open(fname,'wb') as file:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
    progress_bar.close()

             

def downloadrecording(recording_list, name, course_uuid):
      for recording in recording_list:
        recording_data = webService.get_recording_data(recording['recording_id'])
        filename = name + ' - ' + recording['recording_name'].replace(':', ' ').replace('/', ' ').replace('”', '').replace('“', '').replace(',', '').replace('?', '') + '.mp4'
        fullpath = './downloads/'
        print(fullpath + filename)
        descargarGrabacion(recording_data['extStreams'][0]['streamUrl'],fullpath + filename)
       



#Principal modulo:
webService = WebService()
#Conseguir los UUID de cursos basado en Course_ID
cursos_id = ['tga-alberto-ultra','coding0001','2020Fin001']
course_uuids = []
for curso in cursos_id:
    course_uuids.append(webService.getUUID(curso)) 
print("##### UUID CURSOS #######")
print(course_uuids)

tiempo = datetime.datetime.now() - datetime.timedelta(weeks=12)
tiempo = tiempo.strftime('%Y-%m-%dT%H:%M:%SZ')
print("##### Grabaciones  #######")
for cuuid in course_uuids:
    grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
    grabaciones = listaGrabaciones(grabacionesJson)
    if grabaciones is None:
        print("No hay granaciones: " + cuuid)
    else:
        downloadrecording(grabaciones,cuuid,cuuid)
        
