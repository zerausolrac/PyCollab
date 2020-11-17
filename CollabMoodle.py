import datetime
from webService import WebService
import Utilidades as ut
import sys


if __name__ == "__main__":
    param = ut.mainMoodle(sys.argv[1:])
    webService = WebService()
    report = []
    if param[2] == 0:
        tiempo = ut.semanasAtiempo(12)
    else:
        tiempo = ut.semanasAtiempo(param[2])
    if  param[0] != '' and param[1] == '':
        print("Moodle Sesion Name")
        moodlSession = ut.leerUUID(param[0])
        for sesion in moodlSession:
            nombre_session = webService.get_moodle_sesion_name(sesion)
            if nombre_session == None or nombre_session == ' ':
                print("Session name not found!")
            else:
                print(nombre_session)
                lista_grabaciones = webService.get_moodle_lista_grabaciones(nombre_session)
                if lista_grabaciones is None:
                    print("There's no recording for: " + nombre_session)
                else:
                    for grabacion in lista_grabaciones:
                        report.append([grabacion['recording_id'], grabacion['recording_name'],grabacion['duration'],grabacion['storageSize'],grabacion['created']])
                    ut.downloadrecording(lista_grabaciones,nombre_session,nombre_session)
        print(ut.crearReporte(report))
    elif param[0] == '' and param[1] != '':
        print("Moodle LTI Integration Download:", param[1])
        moodle_ids = ut.leerUUID(param[1])
        contexto_ids = []
        grabaciones_id = []
        for moodle_id in moodle_ids:
            contexto_id = webService.get_moodle_grabaciones_contexto(moodle_id,tiempo)
            contexto_ids.append(contexto_id)
        for ctx_id in contexto_ids:
            grabacionesIds = webService.get_moodle_grabaciones_id(ctx_id)
            grabaciones = ut.listaGrabaciones(grabacionesIds)
            if grabaciones is None:
                print("There's no recording: " + ctx_id)
            else:
                for grabacion in grabaciones:
                    report.append([grabacion['recording_id'], grabacion['recording_name'],grabacion['duration'],grabacion['storageSize'],grabacion['created']])
                ut.downloadrecording(grabaciones,ctx_id,ctx_id)       
        print(ut.crearReporte(report))
     
    