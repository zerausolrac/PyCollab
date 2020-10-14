import datetime
import requests
from tqdm import tqdm 
from tqdm import trange
from webService import WebService
import csv
import sys,getopt
import json
from time import sleep

webService = WebService()

def listaGrabaciones(recordings):
        recordinglist = []
        x=0
        try:
          number_of_recordings = (len(recordings['results']))
          if number_of_recordings <= 0:
             return None
          while x < number_of_recordings:
            if 'storageSize' in recordings['results'][x]:
                recordinglist.append({"recording_id" : recordings['results'][x]['id'], "recording_name" : recordings['results'][x]['name'], "duration":recordings['results'][x]['duration'], "storageSize":recordings['results'][x]['storageSize'],"created": recordings['results'][x]['created']})
            else:
                recordinglist.append({"recording_id" : recordings['results'][x]['id'], "recording_name" : recordings['results'][x]['name'], "duration":recordings['results'][x]['duration'], "storageSize":0,"created": recordings['results'][x]['created']})
            x += 1
          return recordinglist
        except TypeError:
         return None



def calculoPeso(url):
    resp = requests.get(url)
    size = int(resp.headers.get('content-length',0))
    return size 


def descargarGrabacion(url:str, fname:str):
    resp = requests.get(url,stream=True)
    total = int(resp.headers.get('content-length',0))
    progress_bar = tqdm(total=total, unit='iB', unit_scale=True,unit_divisor=1024)
    with open(fname,'wb') as file:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
    progress_bar.close()


def crearArchivoChat(url:str,fname:str):
    chatFile = requests.get(url, stream=True)
    if chatFile.status_code == 200:
        jsonInfo = json.loads(chatFile.text)
        #CSV
        filename =  fname + '.csv'
        header = ["Participant id", "Student Name", "Message"]
        file = open(filename, 'w')
        writer = csv.writer(file)
        writer.writerow(header)
        for jsonRow in jsonInfo:
            writer.writerow([jsonRow['id'],jsonRow['userName'], jsonRow['body']])
        file.close()
        total = int(chatFile.headers.get('content-length',0))
        with tqdm(total=total) as progress_bar:
            for size in trange(total):
                progress_bar.update(size)
        progress_bar.close()
    else:
        print("Chat URL is not valid:", str(chatFile))
    
    

             

def downloadrecording(recording_list, name, course_uuid):
      for recording in recording_list:
        recording_data = webService.get_recording_data(recording['recording_id'])
        filename = name + ' - ' + recording['recording_name'].replace(':', ' ').replace('/', ' ').replace('”', '').replace('“', '').replace(',', '').replace('?', '') + '.mp4'
        chatFileName = 'Chat-' + recording['recording_name']
        fullpath = './downloads/'
        print(fullpath + filename)
        descargarGrabacion(recording_data['extStreams'][0]['streamUrl'],fullpath + filename)
        
        if len(recording_data['chats']) == 0:
            print("No chat on the recording.")
        else:
            print("Downloaling chat")
            downloadChats(recording_data['chats'][0],fullpath + chatFileName)


def downloadChats(chat_data,name):
    chat_url = chat_data['url']
    crearArchivoChat(chat_url,name)



def crearReporte(reporte):
   filename = './reports/recordingReport.csv'
   header = ["Recording ID", "Recording Name", "Duration", "Storage Size (MB)", "Created Date"]
   file = open(filename, 'w')
   writer = csv.writer(file)
   writer.writerow(header)
   for x in range(len(reporte)):
      registro = reporte[x]
      recording_id = registro[0]
      recording_name = registro[1]
      duration = calcularTiempo(int(registro[2]/1000))
      storage = str(round(float(registro[3])/1000000, 2))
      created = convertirFecha(registro[4])
      writer.writerow([recording_id,recording_name,duration,storage,created])
   file.close()
   return "Report: recordingReport.csv created!"

   


def crearReporteCollab(reporte):
    filename = './reports/Collab_Report.csv'
    headers = [ 'Course ID', 'Course Name','Course UUID', 'Recording ID', 'Recording Name','Duration', 'Storage Size (MB)', 'Created Date']
    file = open(filename, 'w')
    writer = csv.writer(file)
    writer.writerow(headers)
    for x in range(len(reporte)):
        registro = reporte[x]
        course_id = registro[0]
        couse_name = registro[1]
        course_uuid = registro[2]
        recording_id = registro[3]
        recording_name = registro[4]
        duration = calcularTiempo(int(registro[5]/1000))
        storageSize = str(round(float(registro[6])/1000000, 2))
        created = convertirFecha(registro[7])
        writer.writerow([course_id,couse_name,course_uuid,recording_id,recording_name,duration,storageSize,created])
    file.close()



def leerCursos(filename):
   cursos = []
   with open(filename) as reader:
      for linea in reader:
         contenido = linea.rstrip()
         cursos.append(str(contenido))
   reader.close()
   return cursos


def leerUUID(filename):
   uuids = []
   with open(filename) as reader:
      for linea in reader:
         contenido = linea.rstrip()
         uuids.append(str(contenido))
   reader.close()
   return uuids


def main(argv):
    archivoCursos = ''
    archivoUUID = ''
    semanas = 0
    try:
        opts,args = getopt.getopt(argv,"hf:e:w:", ["cfile=","ext=","weeks="])
    except getopt.GetoptError:
        print('Collab.py -f <LearnFileName_COURSE_ID.txt> -w <numberOfWeekBehindToSearch>')
        print('Collab.py -e <LearnFileName_COURSE_UUID> -w <numberOfWeekBehindToSearch>')
        
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('Collab.py -f <LearnFileName_COURSE_ID.txt> -w <numberOfWeekBehindToSearch>')
            print('Collab.py -e <LearnFileName_COURSE_UUID> -w <numberOfWeekBehindToSearch>')

            sys.exit()
        elif opt in ('-f', '--cfile'):
            archivoCursos = arg
        elif opt in ('-w', '--weeks'):
            semanas = int(arg)
        elif opt in ('-e', '--ext'):
            archivoUUID = arg
    return [archivoCursos, archivoUUID, semanas]



def mainMoodle(argv):
    moodleSessionID = ''
    moodleLTI = ''
    semanas = 0
    try:
        opts,args = getopt.getopt(argv,"hs:l:w:", ["session=","lti=","weeks="])
    except getopt.GetoptError:
        print("The correct params are:")
        print('CollabMoodle.py -s <MoodlePlugInFileName_SESSION_ID.txt> -w <numberOfWeekBehindToSearch>')
        print('CollabMoodle.py -l <MoodleFileName_LTI.txt> -w <numberOfWeekBehindToSearch>')
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('CollabMoodle.py -s <MoodlePlugInFileName_SESSION_ID.txt> -w <numberOfWeekBehindToSearch>')
            print('CollabMoodle.py -l <MoodleFileName_LTI.txt> -w <numberOfWeekBehindToSearch>')
            sys.exit()
        elif opt in ('-s', '--session'):
            moodleSessionID = arg
        elif opt in ('-l', '--lti'):
            moodleLTI = arg
        elif opt in ('-w', '--weeks'):
            semanas = int(arg)
    return [moodleSessionID, moodleLTI, semanas]



def mainReport(argv):
    archivoCursos = ''
    try:
        opts,args = getopt.getopt(argv,"hf:", ["cfile="])
    except getopt.GetoptError:
        print('CollabReport.py -f <LearnFileName_COURSE_ID.txt>')
        
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('CollabReport.py -f <LearnFileName_COURSE_ID.txt>')
            sys.exit()
        elif opt in ('-f', '--cfile'):
            archivoCursos = arg
        

    return [archivoCursos]







def calcularTiempo(s):
   m, s = divmod(s,60)
   h,m = divmod(m,60)
   d, h = divmod(h,24)
   tiempoEnSesion =  datetime.time(h,m,s)
   return tiempoEnSesion.strftime('%H:%M:%S')


def convertirFecha(fecha):
   objetoFecha = datetime.datetime.strptime(fecha,'%Y-%m-%dT%H:%M:%S.%fZ')
   return objetoFecha.strftime('%b %d,%Y')


def semanasAtiempo(weeks):
    tiempo = datetime.datetime.now() - datetime.timedelta(weeks=int(weeks))
    tiempo = tiempo.strftime('%Y-%m-%dT%H:%M:%SZ')
    return tiempo