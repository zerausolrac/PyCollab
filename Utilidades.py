import datetime
import requests
from tqdm import tqdm 
from webService import WebService

webService = WebService()

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
       
