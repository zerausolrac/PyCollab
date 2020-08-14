import datetime

class Session():

    def __init__(self, name, description, survey_url):

        self.sessionJson = {
            "createdTimezone" : "America/New_York",
            "allowInSessionInvitees": 'true',
            "guestRole": "presenter",
            "openChair": 'true',
            "sessionExitUrl": survey_url,
            "mustBeSupervised": 'false',
            "noEndDate": 'true',
            "description": description,
            "canPostMessage": 'true',
            "participantCanUseTools": 'true',
            "courseRoomEnabled": 'false',
            "canAnnotateWhiteboard": 'true',
            "canDownloadRecording": 'true',
            "canShareVideo": 'true',
            "name": name,
            "raiseHandOnEnter": 'false',
            "allowGuest": 'true',
            "showProfile": 'true',
            "canShareAudio": 'true',
            "startTime" : str(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            "boundaryTime" : 15,
            "occurrenceType" : 'S'
        }
    
    def getSessionJson(self):
        return(self.sessionJson)