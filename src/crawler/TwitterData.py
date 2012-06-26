class TwitterData:
    username = None
    userID = 0
    followerID = None
    followerPos = None
    def __init__(self, username, userID, followerID, followerPos):
        self.username = username
        self.userID = userID
        self.followerID = list(followerID)
        self.followerPos = list(followerPos)
