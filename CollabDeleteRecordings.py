import datetime
from webService import WebService
import Utilidades as ut
import sys


if __name__ == "__main__":
    param = ut.mainDelete(sys.argv[1:])
    webService = WebService()
    report = []
    if  param[0] != '':
        recodingsids = ut.listRecordingids(param[0])
        for recording in recodingsids:
            if ut.deleteRecording(recording) == True:
                print(recording + ' was deleted.')
                report.append([recording, 'deleted'])
            if ut.deleteRecording(recording) == False:
                print(recording + ' not found.')
                report.append([recording, 'not found'])
            elif ut.deleteRecording(recording) == None:
                print(recording + ' error: not found')
                report.append([recording, 'not found'])
        if len(report) > 0: 
            print(ut.crearReporteDelete(report))
        else:
            print('No deletions was executed')
    else:
        print("Error, missing argument (list of recordings id file)")