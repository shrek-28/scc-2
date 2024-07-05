from geopy.geocoders import OpenCage
from geopy.distance import geodesic


geolocator = OpenCage(api_key='e2c41cac1abd48929b9bafb46bd619df')

address1 = "address1"
address2 = "address2"

# Geocode the address
def locator(address1, address2):
    location1 = geolocator.geocode(address1)
    location2 = geolocator.geocode(address2)
    lat1 = location1.latitude
    lat2 = location2.latitude
    lon1 = location1.longitude
    lon2 = location2.longitude

    origin = (lat1, lon1)
    destination = (lat2, lon2)

    distance = geodesic(origin, destination).km
    return round(distance,2)
