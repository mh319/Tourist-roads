import geopy
from geopy.geocoders import Nominatim
from geopy.geocoders import GeoNames

def reverse_geo_address(coordinates):
    '''Function that makes an API call through Nominatim for an address given coordinates.'''
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.reverse(coordinates)
    try:
        municipality = location.raw['address']['municipality']
    except:
        municipality = ''
    try:
        postcode = location.raw['address']['postcode']
    except:
        postcode = ''
    try:
        county = location.raw['address']['county']
    except:
        county = ''
    try:
        hamlet = location.raw['address']['hamlet']
    except:
        hamlet = ''
    return municipality, postcode, county, hamlet


def reverse_geo(coordinates):
    '''Function that makes an API call to geonames and returns the closest toponyms geonameID from the coordinates.'''
    # I think for the purpose of this assignment my account-name can be freely used
    # There should be up to 300+ API calls an hour available for free, this one is less then a hundred.
    locator = GeoNames(username='Zuxul')
    location = locator.reverse(query=(coordinates))
    name = location.raw['toponymName']
    geoID = location.raw['geonameId']
    return name, geoID