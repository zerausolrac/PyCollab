import datetime
from webService import WebService
import Utilidades as ut
import sys


if __name__ == "__main__":
    param = ut.main(sys.argv[1:])
    webService = WebService()
    cursos_id = ut.leerCursos(param[0])
    report = []
    course_uuids = []
    for curso in cursos_id:
        course_uuids.append(webService.getUUID(curso)) 
    tiempo = datetime.datetime.now() - datetime.timedelta(weeks=param[1])
    tiempo = tiempo.strftime('%Y-%m-%dT%H:%M:%SZ')
    print("Recordings:")
    for cuuid in course_uuids:
        grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
        grabaciones = ut.listaGrabaciones(grabacionesJson)
        if grabaciones is None:
            print("There's no recording: " + cuuid)
        else:
            for grabacion in grabaciones:
                report.append([grabacion['recording_id'], grabacion['recording_name'],grabacion['duration'],grabacion['storageSize'],grabacion['created']])
            #ut.downloadrecording(grabaciones,cuuid,cuuid)       
    print(ut.crearReporte(report))
    
        







