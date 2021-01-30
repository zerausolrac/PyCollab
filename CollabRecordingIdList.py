import datetime
from webService import WebService
import Utilidades as ut
import sys


if __name__ == "__main__":
    param = ut.mainRecfromid(sys.argv[1:])
    webService = WebService()
    report = []
    report_403 = []
    if  param[0] != '':
        print("Downloading from Collab Recording Ids list...")
        recodingsids = ut.listRecordingids(param[0])
        for recording in recodingsids:
            grabacion = webService.get_grabacion_uuid_data(recording)
            if grabacion != None:
                recording_lista = ut.listaGrabacionCollabData(grabacion)
                recording_lista['recording_id'] = recording
                ut.downloadOneRecordingOnly(recording_lista)
                report.append([recording_lista['recording_id'], recording_lista['recording_name'],recording_lista['duration'],recording_lista['size'],recording_lista['created']])
            else:
                report_403.append([recording_lista['recording_id'],recording_lista['recording_id'], recording_lista['recording_name'],'403 - private recording'])
        if len(report) > 0: 
            print(ut.crearReporteCollabRecIdDownload(report))
        else:
            print('No downloading was executed')
        if len(report_403) > 0:
            print(ut.crearReporte_403(report_403))
        else:
            print('No private recording was found')
    else:
        print("Error, missing argument (list of recordings id file)")