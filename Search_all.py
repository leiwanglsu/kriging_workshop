import datetime
import ee
#this cell is the function of sampling image bands by points
def SampleSentinelImage(img, points,scale=30):
    ft = img.select(['B2','B3','B4','B8A','B11','B12'],['B1','B2','B3','B4','B5','B7']).reduceRegions(points, ee.Reducer.first(),scale) 
    return  ft
def SampleLC08Image(img, points,scale=30):
    ft = img.select(['B2','B3','B4','B5','B6','B7'],['B1','B2','B3','B4','B5','B7']).reduceRegions(points, ee.Reducer.first(),scale) 
    return  ft
def SampleLT57Image(img, points,scale=30):
    ft = img.select(['B1','B2','B3','B4','B5','B7'],['B1','B2','B3','B4','B5','B7']).reduceRegions(points, ee.Reducer.first(),scale) 
    return  ft
#function: check if LC8 product is available and cloud free
def Landsat8Availability(ee,dt, lat,lon,delta,cloud='true'):
    LC8_header = 'LANDSAT/LC08/C01/T1_SR'
    #delta = datetime.timedelta(days = 2)
    if delta.days == 0:
        start = dt
        
        end = dt + datetime.timedelta(days = 1)
    else:
        start = dt - delta
        end = dt + delta
    date1 = ee.Date.fromYMD(start.year, start.month, start.day)
    date2 = ee.Date.fromYMD(end.year, end.month, end.day)    
    roi = ee.Geometry.Point(lon, lat)
    images = ee.ImageCollection(LC8_header) \
        .filterBounds(roi) \
        .filterDate(date1, date2) \
        .sort('CLOUDY_PIXEL_PERCENTAGE')
    try:
        images.getInfo()
    except:
        return 'null'    
    try: 
        image1 = images.first()
    except:
        return("null")
    #check cloud cover at this location on the image
def maskL8sr(image):
# Bits 3 and 5 are cloud shadow and cloud, respectively.
    cloudShadowBitMask = 1 << 3
    cloudsBitMask = 1 << 5

# Get the pixel QA band.
    qa = image.select('pixel_qa')

# Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0) \
        .And(qa.bitwiseAnd(cloudsBitMask).eq(0))

# Return the masked image, scaled to reflectance, without the QA bands.
    return image.updateMask(mask)
        
    if cloud == 'true':
        return maskL8sr(image1)
    else:
        return image1
def cloudMaskL457(image):
    qa = image.select('pixel_qa')
# If the cloud bit (5) is set and the cloud confidence (7) is high
# or the cloud shadow bit is set (3), then it's a bad pixel.
    cloud = qa.bitwiseAnd(1 << 5) \
        .And(qa.bitwiseAnd(1 << 7)) \
        .Or(qa.bitwiseAnd(1 << 3))
# Remove edge pixels that don't occur in all bands
    mask2 = image.mask().reduce(ee.Reducer.min())
    return image.updateMask(cloud.Not()).updateMask(mask2)
def Landsat5Availability(ee,dt, lat,lon,delta,cloud='true'):
    LTHeader = 'LANDSAT/LT05/C01/T1_SR' 
    if delta.days == 0:
        start = dt
        
        end = dt + datetime.timedelta(days = 1)
    else:
        start = dt - delta
        end = dt + delta
    date1 = ee.Date.fromYMD(start.year, start.month, start.day)
    date2 = ee.Date.fromYMD(end.year, end.month, end.day)
    roi = ee.Geometry.Point(lon, lat)
    images = ee.ImageCollection(lt_header) \
        .filterBounds(roi) \
        .filterDate(date1, date2) \
        .sort('CLOUDY_PIXEL_PERCENTAGE')
    #check cloud cover at this location on the image
    try:
        images.getInfo()
    except:
        return 'null'
    try: 
        image1 = images.first()
        image1.getInfo()
    except:
        return("null")
    if cloud=='true':
        return cloudMaskL457(image1)
    else:
        return image1    

def Landsat7Availability(ee,dt, lat,lon,delta,cloud='true'):
    LEHeader = 'LANDSAT/LE07/C01/T1_SR' 
    if delta.days == 0:
        start = dt
        
        end = dt + datetime.timedelta(days = 1)
    else:
        start = dt - delta
        end = dt + delta
    date1 = ee.Date.fromYMD(start.year, start.month, start.day)
    date2 = ee.Date.fromYMD(end.year, end.month, end.day)
    roi = ee.Geometry.Point(lon, lat)
    images = ee.ImageCollection(LEHeader) \
        .filterBounds(roi) \
        .filterDate(date1, date2) \
        .sort('CLOUDY_PIXEL_PERCENTAGE')
    #check cloud cover at this location on the image
    try:
        images.getInfo()
    except:
        return 'null'
    try: 
        image1 = images.first()
        image1.getInfo()
    except:
        return("null")
    if cloud=='true':
        return cloudMaskL457(image1)
    else:
        return image1     
    
# Add Earth Engine dataset
# This example uses the Sentinel-2 QA band to cloud mask
# the collection.  The Sentinel-2 cloud flags are less
# selective, so the collection is also pre-filtered by the
# CLOUDY_PIXEL_PERCENTAGE flag, to use only relatively
# cloud-free granule.
def maskS2clouds(image):
    qa = image.select('QA60')
    # Bits 10 and 11 are clouds and cirrus, respectively.
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11

    # Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(
                qa.bitwiseAnd(cirrusBitMask).eq(0))

    # Return the masked and scaled data
    return image.updateMask(mask)
def sentinel2Availability(ee,dt, lat,lon,delta,cloud='true'):
# Function to mask clouds using the Sentinel-2 QA band.
    
    
    #use gee map sentinel2_timeseries to find the image
    #sentinel2_timeseries(roi=None, start_year=2015, end_year=2019, start_date='01-01', end_date='12-31'):
    #imgs = sentinel2_timeseries(ee.Geometry.Point(lon,lat),date.year,date.year,'{:02d}-{:02d}'.format(date.month,date.day))
    roi = ee.Geometry.Point(lon, lat)
    if delta.days == 0:
        start = dt
        
        end = dt + datetime.timedelta(days = 1)
    else:
        start = dt - delta
        end = dt + delta
    
    date1 = ee.Date.fromYMD(start.year, start.month, start.day)
    date2 = ee.Date.fromYMD(end.year, end.month, end.day)

    #print(date1,date2)
    images = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(roi) \
        .filterDate(date1, date2) \
        .sort('CLOUDY_PIXEL_PERCENTAGE')
#imgs = sentinel2_timeseries(ee.Geometry.Point(lon,lat),date.year,date.year,'{:02d}-{:02d}'.format(date.month,date.day))

    try:
        images.getInfo()
    except:
        return 'null'
    image1 = images.first()
    try:
        image1.getInfo()
    except:
        return 'null'    
    if cloud=='true':
        return maskS2clouds(image1)
    else:
        return image1
        #change the column numbers here for date, lat, and lon
def Search_pixel(ee,locations,delta,cloud,keyword,funcSearch,funcSample,col_lat=4,col_lon=5,col_date=7):
    for datarow in locations[0:1].itertuples():
        print('row number ' + '0')
        img = 'nothing'
        #print(row[2],row[3],row[4],row[5],row[6],row[8])
        #21 33 38.4453 -85.2814 5/1/2013 19.23
        pnt_date = datetime.datetime.strptime(datarow[col_date],'%m/%d/%Y')
        lat = datarow[col_lat]
        lon = datarow[col_lon]
        p1 = ee.Geometry.Point([lon,lat])
        feature1 = ee.Feature(p1)
        feature1 = feature1.set('id',0)
        if datarow[8] != 'ND':
            #search sentinel first
            img = funcSearch(ee,pnt_date,lat,lon,delta,cloud)
            if ImageExist(img) == 'true':
                ac_date = ee.Date(img.get('system:time_start')).format('MM/dd/YYYY');
                print('Found a ' + keyword+ ' image for date:',pnt_date,' at date:', ac_date.getInfo()) 
                feature1 = feature1.set('ac_date',ac_date.getInfo())
                date1 = datetime.datetime.strptime(ac_date.getInfo(),'%m/%d/%Y')
                dt = date1.date() - pnt_date.date()
                feature1 = feature1.set('date_diff',dt.days)
                feature1 = feature1.set('spacecraft',img.get('SPACECRAFT_NAME').getInfo())
                ft = funcSample(img,feature1,30)
                continue
    count=0
    for datarow in locations[1:].itertuples():
        count = count + 1
        print('row: ' + str(count))
        lat = datarow[col_lat]
        lon = datarow[col_lon]
        pnt_date = datetime.datetime.strptime(datarow[col_date],'%m/%d/%Y')
        p1 = ee.Geometry.Point([lon,lat])
        feature1 = ee.Feature(p1)
        feature1 = feature1.set('id',count)
        if datarow[8] != 'ND':
            #search sentinel first
            img = funcSearch(ee,pnt_date,lat,lon,delta,cloud)
            #print(img.getInfo())
            if ImageExist(img) == 'true':
            
                ac_date = ee.Date(img.get('system:time_start')).format('MM/dd/YYYY');
                print('Found a ' + keyword+ ' image for date:',pnt_date,' at date:', ac_date.getInfo())  
                feature1 = feature1.set('ac_date',ac_date.getInfo())
                date1 = datetime.datetime.strptime(ac_date.getInfo(),'%m/%d/%Y')
                dt = date1.date() - pnt_date.date()
                feature1 = feature1.set('date_diff',dt.days) 
                feature1 = feature1.set('spacecraft',img.get('SPACECRAFT_NAME').getInfo())
                ftnew = funcSample(img,feature1,30)
                try:
                    ft = ft.merge(ftnew)
                except:
                    ft = ftnew    
                continue
            print('No image was found, skipped')
    return ft

def ImageExist(img):
    try:
        if img.getInfo()==None:
            return 'false'
        else:
            return 'true'
    except:
        return 'false'