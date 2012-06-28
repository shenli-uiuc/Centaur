class MySQLTwitterData:
    screenName = None
    userID = 0
    followerID = None
    location = None
    def __init__(self, userID, screenName,  followerID, location):
        self.screenName = screenName
        self.userID = userID
        self.followerID = list(followerID)
        self.location = location
