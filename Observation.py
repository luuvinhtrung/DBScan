"""
Vinh-Trung Luu for Technical test
"""
class Observation(object):
    """
        returns an '''Observation''' object with the given latitude, longitude, start_time and duration.
    """
    #constructor
    def __init__(self,lat,lon,startTime,duration):
        self.lat = lat
        self.lon = lon
        self.startTime = startTime
        self.duration = duration

    def getDayString(self):
        """
            returns the startTime attribute string in format of dd/mm/yyyy
        """
        dayString = "%s/%s/%s" % (self.startTime.day, self.startTime.month, self.startTime.year)
        return dayString

    def getCoordinateString(self):
        """
            returns the attributes of lon and lat in format of lon_lat
        """
        coordinateString = "%s_%s" % (self.lat, self.lon)
        return coordinateString
