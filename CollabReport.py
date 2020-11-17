import datetime
from webService import WebService
import Utilidades as ut
import sys
#Collaborate Courses Report

if __name__ == "__main__":
   param = ut.mainReport(sys.argv[1:])
   courses_id = ut.leerCursos(param[0])
   if param[1] == 0:
        tiempo = ut.semanasAtiempo(12)
   else:
       tiempo = ut.semanasAtiempo(param[1])
   
   if len(courses_id) != 0:   
      print("Creating Learn-Collaborate Report...")
      webService = WebService()
      course_uuid = []
      course_info = []
      reporte = []
      reporte_403 = []
      course_uuid_recordings = []

      for course_id in courses_id:
         course_info.append(webService.getCourseInfo(course_id))   
         course_uuid.append(webService.getCourseInfo(course_id)['course_uuid'])     

      
      for cuuid in course_uuid:
         grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
         grabaciones = ut.listaGrabaciones(grabacionesJson)
         if grabaciones is None:
            print("There's no recording for UUID: " + cuuid)
            reporte_403.append([
                        cuuid['course_id'],
                        cuuid['couse_name'],
                        cuuid['course_uuid'],
                        '-',
                        '-',
                        'There is no recording for this course'
                     ])
         else:
            for grabacion in grabaciones:
               if 'msg' not in grabacion:
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
               else:
                  recording_data = {cuuid:
                     {
                     'recording_id':grabacion['recording_id'], 
                     'recording_name':grabacion['recording_name'],
                     'msg':403
                     }
                  }
                  course_uuid_recordings.append(recording_data)




      for cuuid in course_info:
         for recording in course_uuid_recordings:
            if cuuid['course_uuid'] in recording:
               if not 'msg' in recording[cuuid['course_uuid']]:
               
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
                  
               else:
                  reporte_403.append([
                     cuuid['course_id'],
                     cuuid['couse_name'],
                     cuuid['course_uuid'],
                     recording[cuuid['course_uuid']]['recording_id'],
                     recording[cuuid['course_uuid']]['recording_name'],
                     '403: Not allowed, private recording'
                  ])   
   
      if len(reporte) > 0: 
         print(ut.crearReporteCollab(reporte))
      else:
         print('No recordings was found')

      if len(reporte_403) > 0:
         print(ut.crearReporteCollab_403(reporte_403))
      else:
         print('No private recording was found')  
   else:
      print("list of courses is empty!")   
   print(datetime.datetime.utcnow())
   