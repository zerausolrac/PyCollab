import datetime
from webService import WebService
import Utilidades as ut
import sys


if __name__ == "__main__":
    param = ut.main(sys.argv[1:])
    webService = WebService()
    report = []
    report_403 = []
    course_uuids = []
    if param[2]== 0:
        tiempo = ut.semanasAtiempo(12)
    else:
        tiempo = ut.semanasAtiempo(param[2])
    if  param[0] != '' and param[1] == '':
        print("Course Recordings from " + tiempo)
        cursos_id = ut.leerCursos(param[0])
        for curso in cursos_id:
            course_uuids.append(webService.getUUID(curso))
        for cuuid in course_uuids:
            grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
            grabaciones = ut.listaGrabaciones(grabacionesJson)
            if grabaciones is None:
                print("There's no recording for course: " + cuuid)
            else:
                for grabacion in grabaciones:
                    if 'msg' not in grabacion:
                        ut.downloadOneRecording(grabacion,curso)
                        report.append([curso,grabacion['recording_id'], grabacion['recording_name'],grabacion['duration'],grabacion['storageSize'],grabacion['created']])
                    else:
                        report_403.append([curso,grabacion['recording_id'], grabacion['recording_name'],'403 - private recording'])          
        if len(report) > 0: 
            print(ut.crearReporteCollabDownload(report))
        else:
            print('No downloading was executed')
        if len(report_403) > 0:
            print(ut.crearReporte_403(report_403))
        else:
            print('No private recording was found')

    elif param[0] == '' and param[1] != '':
        print("UUID Recordings:")
        course_uuids = ut.leerUUID(param[1])
        for cuuid in course_uuids:
            grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
            grabaciones = ut.listaGrabaciones(grabacionesJson)
            if grabaciones is None:
                print("There's no recording: " + cuuid)
            else:
                for grabacion in grabaciones:
                    if 'msg' not in grabacion:
                        ut.downloadOneRecording(grabacion,cuuid)
                        report.append([grabacion['recording_id'], grabacion['recording_name'],grabacion['duration'],grabacion['storageSize'],grabacion['created']])
                    else:
                        report_403.append([grabacion['recording_id'], grabacion['recording_name'],'403 - private recording'])       
        if len(report) > 0: 
            print(ut.crearReporteCollabDownload(report))
        else:
            print('No downloading was executed')
        if len(report_403) > 0:
            print(ut.crearReporte_403(report_403))
        else:
            print('No private recording was found')
        