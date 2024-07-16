import json

import numpy
import requests
import itertools
import math
from shapely.geometry import Point, Polygon
from scipy.spatial import ConvexHull

from services.map_services import calculate_initial_compass_bearing, \
    calculate_destination_point, get_convex_hull

OSM_API = "https://overpass-api.de/api/interpreter"


class Building:
    def __init__(self, object_id, distance):
        self.object_id = object_id
        self.nodes = self._get_nodes()
        self.nodes_convex_hull = get_convex_hull(self.nodes)
        self.accident_area = self._get_accident_area(distance)

    def _get_nodes(self):
        print('object get_nodes')
        osm_query = f"""
        [out:json];
        way(id:{self.object_id});
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

    def _get_lines_to_extend(self):
        """Получение прямых для их расширения"""
        lines_to_extend = []
        i = 0
        while i < len(self.nodes_convex_hull):
            ii = i + 1
            while ii < len(self.nodes_convex_hull):
                line = [self.nodes_convex_hull[i], self.nodes_convex_hull[ii]]
                lines_to_extend.append(line)
                ii += 1
            i += 1
        return lines_to_extend

    def _get_accident_area(self, distance):
        lines_to_extend = self._get_lines_to_extend()
        # перемещаем точки в прямой по направлению прямой
        points = []
        for line in lines_to_extend:
            bearing = calculate_initial_compass_bearing(line[0], line[1])
            new_point1 = calculate_destination_point(line[0][0],
                                                     line[0][1],
                                                     bearing + 180,
                                                     distance)
            new_point2 = calculate_destination_point(line[1][0],
                                                     line[1][1],
                                                     bearing,
                                                     distance)
            points.append(new_point1)
            points.append(new_point2)

        # сортируем новые точки
        result = get_convex_hull(points)
        return result

    def point_in_accident_area(self, position: []):
        polygon = Polygon(self.accident_area)
        point = Point(position)
        return polygon.contains(point)



