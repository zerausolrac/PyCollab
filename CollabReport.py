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
      course_uuid_recordings = []
      for cuuid in course_uuid:
         grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
         grabaciones = ut.listaGrabaciones(grabacionesJson)
         if grabaciones is None:
            print("There's no recording for UUID: " + cuuid)
         else:
            for grabacion in grabaciones:
               recording_data ={cuuid:
                  {
                  'recording_id':grabacion['recording_id'], 
                  'recording_name':grabacion['recording_name'],
                  'duration':grabacion['duration'],
                  'storageSize':grabacion['storageSize'],
                  'created':grabacion['created']
                 }
               }
               course_uuid_recordings.append(recording_data)
      for idx in course_info:
         if idx['course_uuid'] != "Invalid":
            cuuid = idx['course_uuid']
            grabaciones = [{'5f34e53c4e0b477da350f2016cc2aa17': {'recording_id': '597f4bf9b9cd49ef8321731d115c1a3b', 'recording_name': 'Coding Apple Swift - recording_2', 'duration': 43000, 'storageSize': 3847552, 'created': '2020-09-02T18:43:08.328Z'}}, {'5f34e53c4e0b477da350f2016cc2aa17': {'recording_id': '5c306a5ec4dd4ddeb46e142d2ff073a9', 'recording_name': 'Coding Apple Swift - recording_3', 'duration': 46000, 'storageSize': 3781862, 'created': '2020-09-09T21:52:11.819Z'}}, {'5f34e53c4e0b477da350f2016cc2aa17': {'recording_id': 'ebbb9fefc22046fc92b09d0a8466fd61', 'recording_name': 'Coding Apple Swift - recording_1', 'duration': 108000, 'storageSize': 8406141, 'created': '2020-09-02T17:34:31.182Z'}}]  
            for internal_cuuid in course_uuid_recordings:
               reporte.append([
                  idx['course_id'],
                  idx['couse_name'],
                  idx['course_uuid'],
                  internal_cuuid[cuuid]['recording_id'],
                  internal_cuuid[cuuid]['recording_name'],
                  internal_cuuid[cuuid]['duration'],
                  internal_cuuid[cuuid]['storageSize'],
                  internal_cuuid[cuuid]['created']
               ])
         else:
            print(idx['course_id'] +  ": Not valid course UUID")
      ut.crearReporteCollab(reporte)
   else:
      print("list of courses is empty!")   
   print("Report created successfully: Collab_report.csv")
   