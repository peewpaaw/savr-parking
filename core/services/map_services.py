import math
import numpy

from scipy.spatial import ConvexHull

EARTH_RADIUS = 6378137


def calculate_initial_compass_bearing(pointA, pointB):
    lat1 = math.radians(pointA[0])
    lon1 = math.radians(pointA[1])
    lat2 = math.radians(pointB[0])
    lon2 = math.radians(pointB[1])

    dLon = lon2 - lon1
    x = math.sin(dLon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(dLon))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 returns values from -180° to +180°
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def calculate_destination_point(lat, lon, bearing, distance):
    bearing = math.radians(bearing)
    lat = math.radians(lat)
    lon = math.radians(lon)

    new_lat = math.asin(math.sin(lat) * math.cos(distance / EARTH_RADIUS) +
                        math.cos(lat) * math.sin(distance / EARTH_RADIUS) * math.cos(bearing))

    new_lon = lon + math.atan2(math.sin(bearing) * math.sin(distance / EARTH_RADIUS) * math.cos(lat),
                               math.cos(distance / EARTH_RADIUS) - math.sin(lat) * math.sin(new_lat))

    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)

    return new_lat, new_lon


def get_convex_hull(points):
    """Получение точек выпуклой оболочки"""
    numpy_points = numpy.array(points)
    hull = ConvexHull(numpy_points)
    hull_indices = hull.vertices
    # ??
    result_points = [points[i] for i in hull_indices]
    return result_points
