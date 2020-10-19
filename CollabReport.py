import datetime
from webService import WebService
import Utilidades as ut
import sys
#Collaborate Courses Report

if __name__ == "__main__":
   param = ut.mainReport(sys.argv[1:])
   courses_id = ut.leerCursos(param[0])
   if len(courses_id) != 0:
      
      print("Creating Learn-Collaborate Report...")
      webService = WebService()
      course_uuid = []
      course_info = []
      reporte = []
      for course_id in courses_id:
         course_info.append(webService.getCourseInfo(course_id))   
         course_uuid.append(webService.getCourseInfo(course_id)['course_uuid'])     
      tiempo = datetime.datetime.now() - datetime.timedelta(weeks=12)
      tiempo = tiempo.strftime('%Y-%m-%dT%H:%M:%SZ')      
      
      print("Courses UUID")
      print(course_uuid)

      course_uuid_recordings = []
      for cuuid in course_uuid:
         grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
         grabaciones = ut.listaGrabaciones(grabacionesJson)
         if grabaciones is None:
            print("There's no recording for UUID: " + cuuid)
         else:
            for grabacion in grabaciones:
               recording_data = {cuuid:
                  {
                  'recording_id':grabacion['recording_id'], 
                  'recording_name':grabacion['recording_name'],
                  'duration':grabacion['duration'],
                  'storageSize':grabacion['storageSize'],
                  'created':grabacion['created']
                 }
               }
               course_uuid_recordings.append(recording_data)

      for cuuid in course_info:
         for recording in course_uuid_recordings:
            if cuuid['course_uuid'] in recording:
               reporte.append([
                  cuuid['course_id'],
                  cuuid['couse_name'],
                  cuuid['course_uuid'],
                  recording[cuuid['course_uuid']]['recording_id'],
                  recording[cuuid['course_uuid']]['recording_name'],
                  recording[cuuid['course_uuid']]['duration'],
                  recording[cuuid['course_uuid']]['storageSize'],
                  recording[cuuid['course_uuid']]['created']
               ])
      ut.crearReporteCollab(reporte)
   else:
      print("list of courses is empty!")   
   print("Report created successfully: Collab_report.csv")
   