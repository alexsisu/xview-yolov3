import pyowm
from pyowm.commons.enums import ImageTypeEnum
from pyowm.agroapi10.enums import SatelliteEnum, PresetEnum
import datetime
from pyowm.commons.http_client import HttpClient

"""
Documentation:
https://agromonitoring.com/api
https://pyowm.readthedocs.io/en/latest/usage-examples-v2/agro-api-usage-examples.html
https://wp.agromonitoring.com/dashboard/satellite

"""

def return_sec_for_date(str_date):
    date_time_obj = datetime.datetime.strptime(str_date, '%Y-%m-%d')
    return int(date_time_obj.timestamp())


print(return_sec_for_date("2020-03-19"))
print(return_sec_for_date("2020-03-21"))

agro_monitoring_api_key = open("/Users/alexsisu/ec2keys/agromonitoring.key").read().strip()
owm = pyowm.OWM(agro_monitoring_api_key)
mgr = owm.agro_manager()
mgr.http_client = HttpClient(timeout=360)

list_of_polygons = mgr.get_polygons()
print(list_of_polygons)
timisoara_airport = mgr.get_polygon('5e8763ecf6e0ca5557709781')
print(timisoara_airport)
print(dir(timisoara_airport))

pol_id = '5e8763ecf6e0ca5557709781'  # your polygon's ID

acq_from = 1500336000  # 18 July 2017 # have to be multiplied with 1000
acq_to = 1508976000  # 26 October 2017
acq_from = return_sec_for_date("2020-01-15")
acq_to = return_sec_for_date("2020-03-21")

img_type = ImageTypeEnum.GEOTIFF # ImageTypeEnum.PNG #ImageTypeEnum.GEGEOTIFF  # the image format type
preset = PresetEnum.TRUE_COLOR  # NDVI  # the preset
sat = SatelliteEnum.LANDSAT_8.symbol  # the satellite

sat = SatelliteEnum.SENTINEL_2.symbol  # the satellite

results = mgr.search_satellite_imagery(pol_id, acq_from, acq_to, img_type=img_type, preset=preset, acquired_by=sat)

print(results)
# download all of the images
satellite_images = []
for result in results:
    sat_image = mgr.download_satellite_image(result)
    satellite_images.append(sat_image)

# get stats for the first image
ct = 0
for sat_image in satellite_images:
    sat_img = satellite_images[0]
    #stats_dict = mgr.stats_for_satellite_image(sat_img)
    #print(stats_dict)
    sat_img.persist("agromonitoring" + str(ct) + ".tif")
    ct += 1
