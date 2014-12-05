#Caroline Ball
#GIS_501
#Lab 7 Twitter API


import TwitterSearch
from TwitterSearch import *
import arcpy
from arcpy import env

tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
tso.set_keywords(['Bieber'])  # let's define all words we would like to have a look for
tso.set_include_entities(False)  # and don't give us all those entity information
tso.set_geocode(47.2414, -122.4594, 250, False)  # set the range for twitter data locations

#object creation with secret token
ts = TwitterSearch(
    consumer_key = 'rAqvHaZOVJXsV5OjMV0tZZ7rB',
    consumer_secret = 'wRjIfbaHdanOskIhLfI6RCTRFUJPoGvA6HwXAnnyI4Da61oUuh',
    access_token = '223480230-AoISHI4h06lCgLG2rL82oA0bU8CzorF3YXEipj6R',
    access_token_secret = 'xny88cecmmBAB0bXzLSjtxZgrOkL23bM5Q3L93jmAbJN1')

env.workspace = "E:\GIS_501\Lab_7\Results"
arcpy.env.overwriteOutput = True
fc = "tweetme.shp"

coordsys = 4152  # GCS_North_American_1983_HARN = 4152 (factory code)
spat_ref = (coordsys)  # spatial reference = GCS_North_American_1983_HARN

# create new feature class - define as a point and call the spatial reference
arcpy.CreateFeatureclass_management("E:\GIS_501\Lab_7\Results", "tweetme", "POINT", "", "", "", spat_ref)

# create fields in the attribute table
arcpy.AddField_management(fc, "TWEETED_BY", "TEXT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "POSTED", "TEXT", "", "", 100, "", "NULLABLE")
arcpy.AddField_management(fc, "USER_NAME", "TEXT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "LAT", "FLOAT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "LONG", "FLOAT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "DATE", "TEXT", "", "", 30, "", "NULLABLE")

# use insert cursor to create rows for each of the points
in_curs = arcpy.da.InsertCursor("E:\GIS_501\Lab_7\Results\tweetme.shp", ["SHAPE@XY"])

# iterate through selected tweets
for tweet in ts.search_tweets_iterable(tso):
    if tweet['place'] is not None:
        # use update cursor to poulate rows with tweet data
        up_curs = arcpy.da.UpdateCursor("E:\GIS_501\Lab_7\Results\tweetme.shp",  
                                      ["TWEETED_BY", "POSTED", "USER_NAME", "LAT", "LONG", "DATE"]) 
        cords = (tweet['coordinates'])
        list_cords = list(reduce(lambda x, y: x + y, cords.items()))
        xy = list_cords[3]
        var1 = []
        cord_loc = xy[1], xy[0]
        var1.append(cord_loc)
        in_curs.insertRow(var1)
        tweeted_by = (tweet['user']['name'])
        posted = (tweet['text'])
        user_name = (tweet['user']['screen_name'])
        lat = xy[1]
        lon = xy[0]
        loc = (tweet['created_at'])

        for row in up_curs:
            if row[0] == " ":
                row[0] = tweeted_by
                up_curs.updateRow(row)
            elif row[1] == " ":
                row[1] = posted
                up_curs.updateRow(row)
            elif row[2] == " ":
                row[2] = user_name
                up_curs.updateRow(row)
            elif row[3] == 0:
                row[3] = lat
                up_curs.updateRow(row)
            elif row[4] == 0:
                row[4] = lon
                up_curs.updateRow(row)
            elif row[5] == " ":
                row[5] = loc
                up_curs.updateRow(row)

