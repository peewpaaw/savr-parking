// src/MapComponent.js
import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, Polygon } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Устанавливаем иконку для маркера
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const MapComponent = ({ coordinates, polygons, polygons_ext, noParking}) => {
    const { lat, lng } = coordinates;
    console.log("2poly[]")
    console.log(polygons)
    console.log("2poly2:")
    console.log(polygons_ext)
    const noparking = noParking;
    console.log(noParking)
    const MapUpdater = ({ coordinates }) => {
    const map = useMap();
    useEffect(() => {
        map.setView([coordinates.lat, coordinates.lng], map.getZoom(100));
    }, [coordinates, map]);

    return null;
    };

  return (
    <MapContainer center={[lat, lng]} zoom={13} style={{ height: '100%', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <Marker position={[lat, lng]}>
        <Popup>
          Координаты: {lat}, {lng} <br></br>
          Запрет парковки: {noparking ? "да" : "нет"}
        </Popup>
      </Marker>
      {polygons.map((polygon, index) => (
        <Polygon key={index} positions={polygon} color="blue" />
      ))}
      {polygons_ext.map((polygon, index) => (
        <Polygon key={index} positions={polygon} color="red" />
      ))}
      {/* {polygon_ext && <Polygon positions={polygon_ext} color="red" />} */}
      <MapUpdater coordinates={coordinates} />
    </MapContainer>
  );
};

export default MapComponent;
