

class User():

    def __init__(self, firstName, lastName, displayName, extId, email):

        self.id = None
            
        if lastName != None:
            self.lastName = lastName
        else:
            self.lastName = None
        
        if firstName != None:
            self.firstName = firstName
        else:
            self.firstName = None
        
        if displayName != None:
            self.displayName = displayName
        else:
            self.displayName = None
        
        if extId != None:
            self.extId = extId
        else:
            self.extId = None
        
        if email != None:
            self.email = email
        else:
            self.email = None


    def getId(self):
        
        if id != None:
            return(self.id)
        else:
            return(None)
    
    def setId(self, id):

        self.id = id

    def getLastName(self):
        
        if lastName != None:
            return(self.lastName)
        else:
            return(None)
    
    def setLastName(self, lastName):

        self.lastName = lastName

    def getFirstName(self):
        
        if firstName != None:
            return(self.firstName)
        else:
            return(None)
    
    def setFirstName(self, firstName):

        self.firstName = firstName

    def getDisplayName(self):
        
        if displayName != None:
            return(self.displayName)
        else:
            return(None)
    
    def setDisplayName(self, displayName):

        self.displayName = displayName

    def getExtId(self):
        
        if extId != None:
            return(self.extId)
        else:
            return(None)
    
    def setExtId(self, extId):

        self.extId = extId

    def getEmail(self):
        
        if email != None:
            return(self.email)
        else:
            return(None)
    
    def setEmail(self, email):

        self.email = email

    def getUserJson(self):

        return(
            {
                "id": self.id,
                "lastName": self.lastName,
                "firstName": self.firstName,
                "displayName": self.displayName,
                "extId": self.extId,
                "email": self.email
            }
        )