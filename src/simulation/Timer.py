class Timer:
    #time in seconds
    t = 0

    def __init__(self):
        t = 0

    def cur_time(self):
        return t

    def inc_time(self):
        t += 1

    def inc_time_by(self, sec):
        t += sec
        
