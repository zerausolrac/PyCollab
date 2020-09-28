import datetime
import requests
from tqdm import tqdm 
from webService import WebService
import csv
import sys,getopt

webService = WebService()

def listaGrabaciones(recordings):
        recordinglist = []
        x=0
        try:
          number_of_recordings = (len(recordings['results']))
          if number_of_recordings <= 0:
             return None
          while x < number_of_recordings:
             recordinglist.append({"recording_id" : recordings['results'][x]['id'], "recording_name" : recordings['results'][x]['name'], "duration":recordings['results'][x]['duration'], "storageSize":recordings['results'][x]['storageSize'],"created": recordings['results'][x]['created']})
             x += 1
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
       

def crearReporte(reporte):
   filename = "recordingReport.csv"
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
        print('Collab.py -f <nombreArchivoCursos> -w <semanasAtrasBusqueda>')
        print('Collab.py -e <nombreArchivoUUID> -w <semanasAtrasBusqueda>')
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('Collab.py -f <nombreArchivoCursos> -w <semanasAtrasBusqueda>')
            print('Collab.py -e <nombreArchivoUUID> -w <semanasAtrasBusqueda>')
            sys.exit()
        elif opt in ('-f', '--cfile'):
            archivoCursos = arg
        elif opt in ('-w', '--weeks'):
            semanas = int(arg)
        elif opt in ('-e', '--ext'):
            archivoUUID = arg

    return [archivoCursos, archivoUUID,semanas]


def calcularTiempo(s):
   m, s = divmod(s,60)
   h,m = divmod(m,60)
   d, h = divmod(h,24)
   tiempoEnSesion =  datetime.time(h,m,s)
   return tiempoEnSesion.strftime('%H:%M:%S')


def convertirFecha(fecha):
   objetoFecha = datetime.datetime.strptime(fecha,'%Y-%m-%dT%H:%M:%S.%fZ')
   return objetoFecha.strftime('%b %d,%Y')


