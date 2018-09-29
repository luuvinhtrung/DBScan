"""
Vinh-Trung Luu for Sentiance Technical test
"""
import csv
from dateutil.parser import parse
from Observation import Observation
from math import  sin, cos, sqrt, atan2, radians
from sklearn.cluster import DBSCAN
import pandas as pd
import numpy as np
import scipy
#import matplotlib.cm as cmx
#import matplotlib.colors as colors
#import folium
#import Basemap
#from mpl_toolkits.basemap import Basemap
#import matplotlib.pyplot as plt

#QUESTION 1: Besides the 2 recommended statisticcal summaries, I made 2 additional statistical summaries which are the average duration of visit per
#location and confidence interval of distances between two subsequent stationary locations. There might be other statistical summaries if I had more
#time, for instance the correlation between distance of locations and destination duration, or distribution of start and end time of each move,
#route frequency, ...

def getDateTimeFromString(startTime):
    """
            returns an datetime object, gets original startTime string from .csv file as input.
    """
    try:
        #get year, month, day, hour, min, timeoffset by their corresponding indices (YYYYMMddHHmmZ) in startTime string
        year = startTime[:-13]
        month = startTime[-13:-11]
        day = startTime[-11:-9]
        hour = startTime[-9:-7]
        min = startTime[-7:-5]
        timeoffset = startTime[12:]

        #create valid time string by concatenating year, month, day, hour, min, timeoffset with symbols and blanks
        #to parse to datetime class value
        timeString = year + '/' + month + '/' + day + ' ' + hour + ':' + min + ':' + '00 ' + timeoffset #no sec info then sec value is set to 0
        temp = parse(timeString)
    except Exception as exception:
        print(exception)
        return None

    return parse(timeString)#return parsed string of datetime class

def ParseDataToObsList(filename):
    """
           returns a list of observations of the person as in input .csv file, which is filename param
    """
    observationList = [] #list of the person observations, each obs contains latitude, longitude, start_time and duration as in input file
    file = open(filename)#open and
    reader = csv.reader(file)#read input file of the person
    next(reader, None)#skip file header
    try:
        for e in reader:#e is stored as read line from input in reader
            #get latitude, longitude, start_time and duration at their corresponding indices of e
            lat = e[0]
            lon = e[1]
            startTime = getDateTimeFromString(e[2])
            duration = e[3]
            #create an object of Observation class using extracted latitude, longitude, start_time and duration
            obs = Observation(lat,lon,startTime,duration)
            observationList.append(obs)#and put the object to the observation list
    except IndexError as error:#index error when processing list
        print(error)
        return None
    except Exception as exception:
        print(exception)
        return None
    return observationList

def getVisitedTimeInfoPerDay(observationList):
    """
          returns a dictionary of days as keys and corresponding visited durations as values
    """
    try:
        dayDict = {}#the days and coordinates dictionary
        for obs in observationList:#loop through list of Obsevations objects
            day = obs.getDayString()#get day string of each observation
            duration = obs.duration#get corresponding duration of the observation too
            if day not in dayDict:#if day is not a key in dict yet
                dayDict[day] = [duration]#create element with that key, and add the duration as 1st item list
            else:#otherwise, add the duration to the value list of the existed key
                dayDict[day].append(duration)
    except Exception as exception:
        print(exception)
        return None
    return dayDict

def getVisitedCoordinateInfoPerDay(observationList):
    """
          returns a dictionary of days as keys and corresponding visited coordinates as values
    """
    try:
        dayDict = {}#the days and coordinates dictionary
        for obs in observationList:#loop through list of Observation objects
            day = obs.getDayString()#get day string of each obsevation
            coordinateString = obs.getCoordinateString()#get corresponding coordinate of the observation too
            if day not in dayDict:#if day is not a key in dict yet
                dayDict[day] = [coordinateString]#create element with that key, and add the coordinate as 1st item list
            else:#otherwise, add the coordinate to the value list of the existed key
                dayDict[day].append(coordinateString)
    except Exception as exception:
        print(exception)
        return None
    return dayDict

def getAvgNumVisitedPlacesPerDay(fileName):
    """
          returns the average number of places visited per day of the person
    """
    try:
        observationList = ParseDataToObsList(fileName)
        dayDict = getVisitedCoordinateInfoPerDay(observationList)
        placeCount = 0#initialize the count of visited place of the person, who is parameterized as fileName
        for k,v in dayDict.items():#loop through the dictionary of days as keys and corresponding visited coordinates as values
            placeCount+=len(v)#increase count by visited place number of each day
        avgNumVisitedPlacesPerDay = placeCount/(len(dayDict))#divide the through count by number of days
    except Exception as exception:
        print(exception)
        return None
    return avgNumVisitedPlacesPerDay

def getAvgVisitedTimePerPlaceInMin(fileName):
    """
          returns the median distance traveled between two subsequent stationary locations
    """
    try:
        observationList = ParseDataToObsList(fileName)
        dayDict = getVisitedTimeInfoPerDay(observationList)
        placeCount = 0
        timeCount = 0
        for k, v in dayDict.items():
            placeCount += len(v)
            timeCount += sum(int(x) for x in v)
        timeCountInMin = timeCount/(1000*60)
        if placeCount!=0:
            avgVisitedTimePerPlaceInMin = timeCountInMin/placeCount
        else:
            print("No visited place")
            return None
    except Exception as exception:
        print(exception)
        return None
    return avgVisitedTimePerPlaceInMin

def getDistanceBtw2CoordinatesInKm(point1,point2):
    """
        return the distance in km of subsequent location pair
    """
    try:
        R = 6373.0# approximate radius of earth in km
        point1 = point1.split("_")#split strings of first
        point2 = point2.split("_")#and second coordinates in lat_lon format

        # then get these latitude and longitude values in radian
        lat1 = radians(float(point1[0]))
        lon1 = radians(float(point1[1]))
        lat2 = radians(float(point2[0]))
        lon2 = radians(float(point2[1]))
        # get the distances of longitudes and latitudes
        londist = lon2 - lon1
        latdist = lat2 - lat1
        # calculate the distance in km unit
        a = sin(latdist / 2) ** 2 + cos(lat1) * cos(lat2) * sin(londist / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R*c
    except TypeError as error:
        print(error)
        return None
    except Exception as exception:
        print(exception)
        return None
    return distance

def calculateListMedian(list):
    """
        return the median value of a given list
    """
    try:
        list = sorted(list)#list must be sorted to pick the median up
    except AttributeError as error:
        print(error)
        return
    listLen = len(list)#get list length
    if listLen < 1:#if list is null
        return None
    if listLen % 2 == 0 :#if the number of list elements is even
        return (list[(listLen-1)//2] + list[(listLen+1)//2])/2.0#median is the average of 2 centered element values
    else:#otherwise,
        return list[(listLen-1)//2]#median is the centered element value

def confidenceInterval(data, confidence):
    """
    returns confidence interval value of given numerical list and the level as confidence param
    """
    a = 1.0*np.array(data)#convert data to numpy array
    n = len(a)#length of list
    se = np.std(a,ddof = 1)#standard deviation/error
    h = se * scipy.stats.norm.ppf(1-(1 - confidence)/2.) / np.sqrt(n)#calculate the confidence interval
    return h

def getMedianAndConfidenceIntervalOfDistBtw2SubsqLocation(fileName):
    """
          returns the median distance traveled between two subsequent stationary locations
    """
    try:
        observationList = ParseDataToObsList(fileName)
        dayDict = getVisitedCoordinateInfoPerDay(observationList)
        distList = []#initialize the list of distances between subsequent location pair of the person, who is parameterized as fileName
        for k,v in dayDict.items():#loop through the dictionary of days as keys and corresponding visited coordinates as values
            for i in range(len(v)-1):#loop through the list of day visited coordinates
                dist = getDistanceBtw2CoordinatesInKm(v[i],v[i+1])#get the distance in km of subsequent location pair
                distList.append(dist)#and add the distance to distance list
        medianDistBtw2SubsqLocation = calculateListMedian(distList)
        cIValue = confidenceInterval(distList,0.95)
    except IndexError as error:#index error when processing list
        print(error)
        return None
    except Exception as exception:
        print(exception)
        return None
    return medianDistBtw2SubsqLocation,cIValue

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#QUESTION 2: Assuming that a location visit is not time constrained, I put the duration info aside and focus on the coordinates. As it said
#"some noise is added to the longitude/latitude pairs", I suggest to define a location as a zone, not a single coordinate. For coordinate
#clustering, DBSCAN is an effective and popular method. Accordingly, we can cluster coordinates using the person data with params like 0.2 km is
#the maximum distance to be in the same cluster, and it takes at least 2 coordinates to be a zone. That maximum distance is reasonable to form
#a popular location like building, bar, home... including long/lat noise. These params can be changed due to the domain knowledge.

#Consequently, it forms a list of visited locations that can be defined by maximum latitude, maximum longitude, minimum latitude, minimum longitude
#as a rectangles on map. These rectangles are not likely overlap and can be used to check whether or not a user has ever visited a location, as follows:
#Create a lookup table containing columns of maximum latitude, maximum longitude, minimum latitude and minimum longitude. Accordingly, for each user
#coordinate as input, if #maximum latitude >= its latitude >= minimum latitude and maximum longitude >= its longitude >= minimum longitude then that
#coordinate/location was visited. Otherwise, it is not visited yet. The stopping criteria of the loop is when the coordinate is found to be visited
#or the table is through. A dataframe is adopted to build a lookup table. For the lookup function, please see the next question's answer.

#The complexity of memory and performance of DBSCAN algorithm and table lookup are taken into account:

#For DBSCAN, it possibly hits every single coordinate multiple times to see if it is the core of cluster, then given n the number of points, Time
#complexity can reach O(n**2), and can be improved to O(nlog(n))by choosing appropriate epsilon. DBSCAN can run without distance matrix and hence,
#the space complexity should be O(n) as it only need to know the positions of n coordinates during the run.

#For table lookup, it can reach O(m), given m the number of cluster or table row.

#Again, and also for the next question, clusters of coordinates are used to deal with 1)The location area and 2)The coordinate noise

def getCoordinateList(fileName):
    """
    returns list of coordinates visited by the person
    """
    df = pd.DataFrame.from_csv(fileName,index_col=None)#no index column to read
    coordinateList = df.as_matrix(columns=['latitude', 'longitude'])#list contains 2 columns of latitude and longitude
    return coordinateList

def getMinMaxCoorsOfCluster(coorSerie):
    """
    returns list of maximum latitude, maximum longitude, minimum latitude and minimum longitude
    """
    lat = []#latitude list of coordinates in cluster
    lon = []#longitude list of coordinates in cluster
    for coor in coorSerie:#lats and lons are extracted from coordinate list
        lat.append(coor[0])#and put in corresponding lat/lon list
        lon.append(coor[1])
    return np.amax(lat),np.amax(lon),np.amin(lat),np.amin(lon)


def createLookupTableForVisitCheck(fileName,min_samples,km_eps):
    """
        returns lookup table to check if a coordinate is in a visited location
    """
    coordinateList = getCoordinateList(fileName)
    #coordinateList = observationList[]
    R = 6373.0 # approximate radius of earth in km
    epsilon = km_eps/R#corresponding radian value of 0.2 km

    # Parameterize DBSCAN anf fit it with coordinate list
    db = DBSCAN(eps=epsilon,min_samples=min_samples,algorithm='ball_tree',metric='haversine').fit(np.radians(coordinateList))
    cluster_labels = db.labels_#get labels of clusters created (cluster_labels = -1 means outliers that don't belong to any cluster)
    n_clusters = len(set(cluster_labels))#get number of clusters created

    #get the series of cluster containing corresponding coordinates
    clusters = pd.Series([coordinateList[cluster_labels == n] for n in range(-1, n_clusters)])
    lookupTable = pd.DataFrame(columns=["MaxLat", "MaxLon", "MinLat", "MinLon"])#create lookup table as a dataframe
    for cl in clusters:
        if len(cl)>0:
            maxLat, maxLon, minLat, minLon = getMinMaxCoorsOfCluster(cl)#get min and max of lat and lon of each cluster
            row = pd.DataFrame({"MaxLat": [maxLat], "MaxLon": [maxLon], "MinLat": [minLat], "MinLon": [minLon]})
            lookupTable = lookupTable.append(row)#then add them to the table as a new row
    return lookupTable

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#QUESTION 3: Besides home and work locations, a person may have other interest points like coffee shop, supermarket, sport center,... that take part
#in the recorded data. I suggest to take advantage of the lookup table in Question 2 to see which locations the person spent time, how long, which
#weekday and their start time. A prediction can be made based on these kind of information, for example, if they spend weekends at some locations,
#with late start time and during a long time, those locations are likely home. Alternatively, a work place is often "checked-in" on weekdays, in the
#mornings and during a not very long time. They possibly visit other interest points as mentioned below at times during the day, in a short time...
#As a consequent, looking at a specific location with such user information, ones can guess what kind of place it may be. For example, using input of
#"Copy of person.2.csv", setting DBSCAN min_samples = 7, km_eps = 0.2, the 2nd cluster of lookup table gathers following information:

#-Location([51.221703000000005,4.414096],[51.210440000000006,4.3912487])
#-Info: ['12:11 Thursday 2.67hr', '14:11 Sunday 0.0hr', '14:46 Saturday 0.0hr', '14:53 Saturday 2.59hr', '17:37 Saturday 0.07hr',
# '23:03 Saturday 1.98hr', '1:19 Sunday 45.33hr', '19:05 Saturday 0.1hr', '19:15 Saturday 0.3hr']

#Then a prediction can be made that this location is likely home, as most of the days spent there are weekends. In contrary, most of the observations
#at 4th cluster are on weekday... Accordingly, a model can be build to predict that way with threshold parameters (if I have more time, and real
#location info to train and test. Furthermore, I would suggest to try ensemble methods such as Random Forest or XGBoosting on features like weekday,
#duration and start time for classification, when working on clusters of the lookup table. XGBoosting is good at time complexity but more likely
#overfitting).

# The reason to choose 7 for min_samples instead of 2 in Question 2 is the locations of work or home are likely frequently visited, so the minimum
#number of cluster points should be greater than an "ever visited" location. As a result, this leads to less but bigger clusters. Not with standing,
#these hyper params can be optimized implementing gradient descent.

#The complexity of memory and performance for this task has been discussed in Question 2 so far, including DBSCAN and lookup.

#For the map visualization, I wanted to use Basemap to show clusters as described in Question 2 with different colors, sizes and other information.
#However, I had a bit problem with Basemap that it is installable but not importable. I think it is fixable with a little additional time.

#Some other features can be taken into account: speed (calculated by distance and time cost between subsequent points), transportation means, age,
#gender, route frequency,... to improve the model prediction accuracy. Alternatively, those features may be predicted using current data.

def dow(date):
    """
        return weekday of a given date
    """
    days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dayNumber=date.weekday()#get weekday from date
    return days[dayNumber]

def detectLikelyHomeAndWorkLocation(fileName):
    """
        returns a dictionary with keys as locations, and values as information of start time,
        weekday and duration the person was supposed to stay there
    """
    lookupTable = createLookupTableForVisitCheck(fileName,7,0.2)#create a lookup table dedicated to the person
    observationList = ParseDataToObsList(fileName)#load the observations of that person
    clusterDict = {}#the output dictionary
    for obs in observationList:#check each observation
        for index, row in lookupTable.iterrows():#to see if the coordinates belong to a listed location
            #print("Row",row)
            if float(obs.lat) <= float(row['MaxLat']) and float(obs.lat) >= float(row['MinLat']) \
            and float(obs.lon) <= float(row['MaxLon']) and float(obs.lon) <= float(row['MinLon']):
                #if the coordinate belongs to a location in lookup table, its dict key is built using max and min of lat and lon
                key = str(row['MaxLat'])+'_'+str(row['MinLat'])+'_'+str(row['MaxLon'])+'_'+str(row['MinLon'])
                #for the dict value, it is formed by start time (hr:mm), duration (in hour), and weekday of the observation
                hr = str(obs.startTime.hour)
                min = str(obs.startTime.minute) if obs.startTime.minute > 9 else '0'+str(obs.startTime.minute)
                hrs = str(round((float(obs.duration)/(1000*3600)),2))
                weekday = str(dow(obs.startTime))
                value = hr + ':' + min +' '+weekday+' '+hrs+'hr'
                if key not in clusterDict:
                    clusterDict[key] = [value]#create new dict element
                else:
                    clusterDict[key].append(value)#or add value to element's values
                break;
    return clusterDict

#getAvgNumVisitedPlacesPerDay("Copy of person.2.csv")
#getAvgVisitedTimePerPlaceInMin("Copy of person.2.csv")
#observationList = ParseDataToObsList("Copy of person.2.csv")
#getMedianAndConfidenceIntervalOfDistBtw2SubsqLocation("Copy of person.2.csv")
#detectLikelyHomeAndWorkLocation("Copy of person.2.csv")
