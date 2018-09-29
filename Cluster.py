class Cluster(object):
    """
        returns a '''Cluster''' object with the given min latitude, max latitude, min longitude, max longitude, start_time and duration.
    """
    #constructor
    def __init__(self,minlat,maxlat,minlon,maxlon,startTime,duration):
        self.minlat = minlat
        self.maxlat = maxlat
        self.minlon = minlon
        self.maxlon = maxlon
        self.startTime = startTime
        self.duration = duration

