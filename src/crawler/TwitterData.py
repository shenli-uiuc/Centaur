class TwitterData:
    screenName = None
    userName = None
    userID = 0
    followerID = None
    followerPos = None
    def __init__(self, userID, screenName, username, followerID, followerPos):
        self.screenName = screenName
        self.userName = username
        self.userID = userID
        self.followerID = list(followerID)
        self.followerPos = list(followerPos)
