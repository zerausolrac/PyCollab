# PyCollab
Python Blackoboard Collaborate script to download recording based on Blackboard Learn courses linked to Blackboard Collaborate session.
and get:
-	Recording Report in a CSV file (Recording_ID, Storage Size, Duration, Creation Date, Duration)
-	Downloads local folder that will receive the MP4 video recording files
-	Command line attributes: 1) to load external file that list courses_id   2)  weeks int value to search for recording  behind current date.




## 1 Instalation
You need to have installed Python 3.7+ 

## 2 Install requirements 
```
pip3 install -r requerimientos.txt
```

## 3 Add Blackboard Collaborate and Learn Credentials
```
edit content of Config.py file
```
### Note

In order to get the Learn credentials, they do not to open a case on behind the blackboard nor email developers@blackboard.com.

They need to go to developer.blackboard.com and register from there to grab the Learn credentials for their application, it is also imperative to remind them that they are creating an application based on your code, so they need to register as a developer.

Now, for Collaborate production they CAN and MUST create a ticket on behind the blackboard requesting their credentials.

## 4 Modify external file depending on scenario
```
edit learn_courses.txt file
edit learn_uuids.txt file
edit moodle_lti_id.txt file
edit moodle_plugin_sessions.txt file
```


## 5 Run the script

<ul>
<li>python3 Collab.py</li>
<li>python3 CollabMoodle.py</li>
<li>python3 CollabReport.py</li>
</ul>


### Search recording from Blackboard Learn to Collaborate   

<li>if you have the Blackboard Learn course id(s) as input data on the file learn_courses.txt, where -w is a value of weeks back for as starting point of searching for recordings:
<li>

```
python3 Collab.py -f learn_courses.txt -w 10   
```
<li>
if you have the Blackboard Learn UUID(s) as input data on the file learn_uuids.txt, where -w is a value of weeks back for as starting point of searching for recordings:
</li>

```
python3 Collab.py -e learn_uuids.txt -w 10   
```


### Search recording from Moodle to Collaborate  

<li>if you have the Moodle session Id created by Moodle Collaborate plugin as input data on the file moodle_plugin_sessions.txt, where -w is a value of weeks back for as starting point of searching for recordings:
<li>

```
python3 CollabMoodle.py -s moodle_plugin_sessions.txt -w 10   
```
<li>
if you have the Moodle courses ID(s) related to Moodle LTL Tool as input data on the file moodle_lti_id.txt, where -w is a value of weeks back for as starting point of searching for recordings:
</li>

```
python3 CollabMoodle.py -l moodle_lti_id.txt -w 10   
```



# Video

<a href="https://www.youtube.com/watch?v=UxKZvBw_-NU" target="new"> 
English
</a>
<br>
<br>
<a href="https://www.youtube.com/watch?v=0ov-HZJeAE0&feature=youtu.be" target="new"> 
Español
</a>