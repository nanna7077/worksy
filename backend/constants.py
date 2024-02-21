import math
from enum import Enum

AUTHENTICATION_HEADER = "Authorization"
SESSION_EXPIRATION_DAYS = 365
DEFAULT_LIST_RADIUS = 10
DEFAULT_SEARCH_LIMIT = 10
DEFAULT_ANNOUNCE_RADIUS = 10

class SystemEventType(Enum):
    ALERT = 0
    WARNING = 1
    ERROR = 2

def getClientIPAddress(request):
    return request.headers.get("X-Forwarded-For", request.remote_addr)

def haversine_add_distance_to_coordinates(lat, lon, distance_km):
    earth_radius = 6371.0

    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    angular_distance = distance_km / earth_radius

    new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(angular_distance) +
                            math.cos(lat_rad) * math.sin(angular_distance) * math.cos(0))

    new_lon_rad = lon_rad + math.atan2(math.sin(0) * math.sin(angular_distance) * math.cos(lat_rad),
                                       math.cos(angular_distance) - math.sin(lat_rad) * math.sin(new_lat_rad))

    new_lat = math.degrees(new_lat_rad)
    new_lon = math.degrees(new_lon_rad)

    return new_lat, new_lon
