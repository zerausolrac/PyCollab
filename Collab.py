import datetime
from webService import WebService
import Utilidades as ut
import sys


if __name__ == "__main__":
    param = ut.main(sys.argv[1:])
    webService = WebService()
    report = []
    course_uuids = []
    if  param[1] == '':
        print("Course Recordings:")
        cursos_id = ut.leerCursos(param[0])
        for curso in cursos_id:
            course_uuids.append(webService.getUUID(curso))
        print(course_uuids)
    else:
        print("UUID Recordings:")
        course_uuids = ut.leerUUID(param[1])
        print(course_uuids)
    tiempo = datetime.datetime.now() - datetime.timedelta(weeks=param[2])
    tiempo = tiempo.strftime('%Y-%m-%dT%H:%M:%SZ')
    for cuuid in course_uuids:
        grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
        grabaciones = ut.listaGrabaciones(grabacionesJson)
        if grabaciones is None:
            print("There's no recording: " + cuuid)
        else:
            for grabacion in grabaciones:
                report.append([grabacion['recording_id'], grabacion['recording_name'],grabacion['duration'],grabacion['storageSize'],grabacion['created']])
            ut.downloadrecording(grabaciones,cuuid,cuuid)       
    print(ut.crearReporte(report))
     
        







