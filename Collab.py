import datetime
from webService import WebService
import Utilidades as ut


webService = WebService()
#Get Course  UUID from Learn Course_Id:
cursos_id = ['tga-alberto-ultra','coding0001','2020Fin001']
course_uuids = []
for curso in cursos_id:
    course_uuids.append(webService.getUUID(curso)) 
print("##### Course UUID #######")
print(course_uuids)

#12 weeks ago, you can modify weeks value as staring search point.
tiempo = datetime.datetime.now() - datetime.timedelta(weeks=12)
tiempo = tiempo.strftime('%Y-%m-%dT%H:%M:%SZ')
print("##### Recordings  #######")
for cuuid in course_uuids:
    grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
    grabaciones = ut.listaGrabaciones(grabacionesJson)
    if grabaciones is None:
        print("There's no recording: " + cuuid)
    else:
        ut.downloadrecording(grabaciones,cuuid,cuuid)