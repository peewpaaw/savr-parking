import requests
import itertools
import math

from shapely.geometry import Point, Polygon


OSM_API = "https://overpass-api.de/api/interpreter"

# Радиус по которому смотрим ближайшие здания
RADIUS = 50
# Радиус Земли
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


# Function to calculate a point given a start point, bearing, and distance
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


def get_min_lines(coords):
    # две точки с наименьшим расстоянием
    min_distance = float('inf')
    closest_points = None

    for pair in itertools.combinations(coords, 2):
        distance = math.hypot(pair[0][0] - pair[1][0], pair[0][1] - pair[1][1])
        if distance < min_distance:
            min_distance = distance
            closest_points = pair
    lines = []
    line1 = list(closest_points)
    line2 = [item for item in coords if item not in line1]
    lines.append(line1)
    lines.append(line2)
    #lines_test = get_rectangle_points(lines)
    return lines

def get_way_nodes(way_id):
    osm_query = f"""
    [out:json];
    way(id:{way_id});
    (._;>;);
    out body;
    """
    url = f"{OSM_API}?data={osm_query}"
    response = requests.get(url)
    node_list = []
    if response.status_code == 200:
        for node in response.json()['elements']:
            if node['type'] == 'node':
                node_list.append((node['lat'], node['lon']))
    return node_list


def get_nearest_buildings(lat, long):
    osm_query = f"""
    [out:json];
    (
      way
        ["building"]
        (around:{RADIUS},{lat},{long});
    );
    out body;
    >;
    out skel qt; 
    """
    url = f"{OSM_API}?data={osm_query}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()['elements']
    return None


def get_rectangle_points(coords: []):
    new_coords = []
    # Get point with min latitude
    min_lat_point = min(coords, key=lambda x: x[0])
    # Get point with max latitude
    max_lat_point = max(coords, key=lambda x: x[0])
    # Get point with min longitude
    min_lon_point = min(coords, key=lambda x: x[1])
    # Get point with max longitude
    max_lon_point = max(coords, key=lambda x: x[1])

    new_coords.append(min_lat_point)
    new_coords.append(min_lon_point)
    new_coords.append(max_lat_point)
    new_coords.append(max_lon_point)

    return new_coords


def polygon_contains_point(coords: [], position: []):
    polygon = Polygon(coords)
    point = Point(position)
    #print(polygon)
    #print(point)
    return polygon.contains(point)


"""ENTRY"""


def entry_point(lat, lon):
    # Получаем ближайшие здания в радиусе от точки
    nearest_buildings = get_nearest_buildings(lat, lon)

    buildings = []
    for build in nearest_buildings:
        build_elem = dict()
        if build['type'] == 'way':
            build_elem['id'] = build['id']
            build_elem['levels'] = 1
            if 'building:levels' in build['tags']:
                build_elem['levels'] = int(build['tags']['building:levels'])
        if bool(build_elem):
            buildings.append(build_elem)

    # Формируем ноды
    for build in buildings:
        build['nodes'] = get_way_nodes(build['id'])
        build['nodes_rect'] = get_rectangle_points(build['nodes'])
        lines_to_extend = get_min_lines(build['nodes_rect'])
        new_lines = []
        for line in lines_to_extend:
            bearing = calculate_initial_compass_bearing(line[0], line[1])
            # Calculate new points by extending the line
            new_point1 = calculate_destination_point(line[0][0],
                                                     line[0][1],
                                                     bearing + 180,
                                                     build['levels']*3)
            new_point2 = calculate_destination_point(line[1][0],
                                                     line[1][1],
                                                     bearing,
                                                     build['levels']*3)
            #new_line = (new_point1, new_point2)
            new_lines.append(new_point1)
            new_lines.append(new_point2)
        build['nodes_rect_ext'] = get_rectangle_points(new_lines)
        build['parking'] = not polygon_contains_point(build['nodes_rect_ext'], [lat, lon])
    print("BUILDINGS: ", buildings)
    return buildings
