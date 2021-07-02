import datetime
def sentinel2Availability(ee, dt, lat, lon, delta, cloud='true'):
# Function to mask clouds using the Sentinel-2 QA band.
          # use gee map sentinel2_timeseries to find the image
    # sentinel2_timeseries(roi=None, start_year=2015, end_year=2019, start_date='01-01', end_date='12-31'):
    # imgs = sentinel2_timeseries(ee.Geometry.Point(lon,lat),date.year,date.year,'{:02d}-{:02d}'.format(date.month,date.day))
    roi = ee.Geometry.Point(lon, lat)
    if delta.days == 0:
        start = dt

        end = dt + datetime.timedelta(days=1)
    else:
        start = dt - delta
        end = dt + delta

    date1 = ee.Date.fromYMD(start.year, start.month, start.day)
    date2 = ee.Date.fromYMD(end.year, end.month, end.day)

    # print(date1,date2)
    images = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(roi) \
        .filterDate(date1, date2) \
        .sort('CLOUDY_PIXEL_PERCENTAGE')
# imgs = sentinel2_timeseries(ee.Geometry.Point(lon,lat),date.year,date.year,'{:02d}-{:02d}'.format(date.month,date.day))

    try:
        images.getInfo()
    except:
        return 'null'
    image1 = images.first()
    try:
        image1.getInfo()
    except:
        return 'null'
    return image1

def ImageExist(img):
    try:
        if img.getInfo()==None:
            return 'false'
        else:
            return 'true'
    except:
        return 'false'
