# PyCollab


Python Blackoboard Collaborate script to download recording based on Blackboard Learn Course ID, or Blackboard Learn Course UUID, Moodle plugin session ID, Moodle LTI Tool.
and get:
<ul>
<li>Recording Report in a CSV file (Recording_ID, Storage Size, Duration, Creation Date, Duration) on /reports folder
</li>
<li>Downloads local folder that will receive the MP4 video <i>if the recording have chats, those will be downloaded too.</i> Recording  and Chat csv files will be on /downloads folder
</li>
<li>Command line attributes depending on the scenario: Learn Course,Blackboard Learn Course UUID, Moodle plugin session ID, Moodle LTI Tool.
</li>
</ul>




## 1. Instalation
You need to have installed Python 3.7+ 

Will depent on Computer operation system how Python is referenced on command line tool:
<br> 
<br> 
- Mac OS: normally python3 is the alias to run python scripts when install python 3.7+
<br>
- Windows OS: normally python is the alias to run python scripts when install python 3.7+
<br>


## 2. Install requirements 
```
pip3 install -r requerimientos.txt
```

## 3. Add Blackboard Collaborate and Learn Credentials
<ul>
<li>scenario 1:  Learn to Collaborate search for recordings</li>
<li>scenario 2: Moodle to Collaborate search for recordings</li>
<li>scenario 3: Collab Admin Institutional Reports</li>
</ul>

<br>
if you have the scenario 1 you need to insert both Learn and Collaborate credentials 
<br>
If you have the scenario 2 or scenario 3, yo only need to insert Collaborate credentials but DO NOT REMOVE the key:value association of Learn credentils section from the Config.py file, you can leave blank

```
edit content of Config.py file
```


### Note

In order to get the Learn credentials, go to developer.blackboard.com and register from there to grab the Learn credentials for their application, it is also imperative to remind them that they are creating an application based on your code, so they need to register as a developer.Then on your Blackboard Learn environment, as admin role user, go to Rest API Integration a create an integration using data provided from developer.blackboard.com before.


Now, for Collaborate production they CAN and MUST create a ticket on behind the blackboard requesting their credentials.

## 4. Modify external file depending on scenario
```
edit learn_courses.txt file
edit learn_uuids.txt file
edit moodle_lti_id.txt file
edit moodle_plugin_sessions.txt file
```


## 5. Run the script

<ul>
<li>Collab.py -h</li>
<li>CollabMoodle.py -h</li>
<li>CollabReport.py -h</li>
<li>CollabMinutes.py -h</li>
<li>CollabRecordings.py -h</li>
<li>CollabRecordingsDownload.py -h</li>
</ul>
<br>
## Scenario 1
### Search recording from Blackboard Learn to Collaborate  

<li>if you have the Blackboard Learn course id(s) as input data on the file learn_courses.txt, where -w is a value of weeks back for as starting point of searching for recordings:
<B>Note:</B> <i>if the recording have chats, those will be downloaded too.</i>
</li>

```
python3 Collab.py -f learn_courses.txt -w 10   
```
<li>
if you have the Blackboard Learn UUID(s) as input data on the file learn_uuids.txt, where -w is a value of weeks back for as starting point of searching for recordings:
<B>Note:</B> <i>if the recording have chats, those will be downloaded too.</i>
</li>

```
python3 Collab.py -e learn_uuids.txt -w 10   
```

<b>Report Learn-Colaborate</b>
<li>
If you need to know about recording storage size, duration and  recording ID before download any recording you can create a report, where -f is point to learn_courses.txt file that have Blackboard Learn courses ID listed by row:
</li>

```
python3 CollabReport.py -f learn_courses.txt
```


## Scenario 2
### Search recording from Moodle to Collaborate  

<li>if you have the Moodle session Id created by Moodle Collaborate plugin as input data on the file moodle_plugin_sessions.txt, where -w is a value of weeks back for as starting point of searching for recordings:
<B>Note:</B> <i>if the recording have chats, those will be downloaded too.</i>
</li>

```
python3 CollabMoodle.py -s moodle_plugin_sessions.txt -w 10   
```
<li>
if you have the Moodle courses ID(s) related to Moodle LTI Tool as input data on the file moodle_lti_id.txt, where -w is a value of weeks back for as starting point of searching for recordings:
<B>Note:</B> <i>if the recording have chats, those will be downloaded too.</i>
</li>

```
python3 CollabMoodle.py -l moodle_lti_id.txt -w 10   
```


## Scenario 3
### Collaborate Admin Institutional Reports 

<b>Report Minutes on Callaborate from AttendeeReport</b>
<li>
if you need to identify the amount of minutes spend in Collaborate session,first  you need to download the Collaborate Admin Institutional Attendance Report according to your zone (ca:Canada, us: USA), then use the script CollabMinutes.py with the parameter -f that point to the file previously downloaded.
</li>
```
python3 CollabMinutes.py -f AttendeeReport.csv   
```

<br>
<br>

<b>Report RecordingId from Collaborate RecordingsReport</b>
<li>
if you need to get information about recordingId, storage size, first you need to download the Collaborate Admin Institutional Recording Report according to your zone (ca:Canada, us: USA), then use the script CollabRecordings.py with the parameter -f that point to the file previously downloaded. 
</li>
```
python3 CollabRecordings.py -f RecordingsReport.csv   
```
<br>
<br>

<b>Download RecordingId from Collaborate RecordingsReport</b>
<li>
if you need to download recordings, first you need to download the Collaborate Admin Institutional Recording Report according to your zone (ca:Canada, us: USA), then use the script CollabRecordingsDownload.py with the parameter -f that point to the file previously downloaded. 
</li>
```
python3 CollabRecordingsDownload.py -f RecordingsReport.csv   
```
<br>
<br>


# Video

<a href="https://www.youtube.com/watch?v=UxKZvBw_-NU" target="new">English</a>
<br>
<br>
<a href="https://www.youtube.com/watch?v=0ov-HZJeAE0&feature=youtu.be" target="new"> Español</a>