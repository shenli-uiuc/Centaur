class Timer:
    #time in seconds
    t = 0

    def __init__(self):
        self.t = 0

    def cur_time(self):
        return self.t

    def inc_time(self):
        self.t += 1

    def inc_time_by(self, sec):
        self.t += sec
        
