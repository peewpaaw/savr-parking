import React, { useEffect } from "react";
import {
  MapContainer,
  Marker,
  Polygon,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

const customIcon = L.icon({
  iconUrl: require("./transport.png"),
  iconSize: [42, 42],
  iconAnchor: [12, 28],
});
const customIconSpeed = L.icon({
  iconUrl: require("./transportRed.png"),
  iconSize: [42, 42],
  iconAnchor: [12, 28],
});

const MapComponent = ({
  coordinates,
  polygons,
  polygons_ext,
  noParking,
  data,
  setState,
}) => {
  const MapUpdater = ({ coordinates }) => {
    const map = useMap();

    useEffect(() => {
      map.flyTo([coordinates.lat, coordinates.lng], map.getMaxZoom(18));
    }, [coordinates, map]);

    return null;
  };

  const handleMarkerClick = async (e) => {
    const response = await fetch(
      `http://127.0.0.1:8000/nearest?lat=${e.latlng?.lat}&lon=${e.latlng?.lng}`,
    );
    const data = await response.json();

    const polygons = data.map((polygon) =>
      polygon.nodes_rect.map(([lat, lng]) => [lat, lng]),
    );
    const polygons_ext = data.map((polygon_ext) =>
      polygon_ext.nodes_rect_ext.map(([lat, lng]) => [lat, lng]),
    );
    const noParking = data.some((item) => item.parking === false);

    await setState({
      coordinates: { lat: e.latlng?.lat, lng: e.latlng?.lng },
      polygons,
      polygons_ext,
      noParking,
    });
  };

  return (
    <MapContainer
      center={[coordinates?.lat, coordinates?.lng]}
      zoom={12}
      whenReady={() => {
        console.log("This function will fire once the map is created");
      }}
      whenCreated={(map) => {
        console.log("The underlying leaflet map instance:", map);
      }}

      style={{ height: "100%", width: "100%" }}
      >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {data?.length &&
        data?.map(
          (el) =>
            el?.latitude && (
              <Marker
                icon={el?.speed > 0 ? customIconSpeed : customIcon}
                eventHandlers={{ click: handleMarkerClick }}
                position={[el?.latitude, el?.longitude]}
              >
                <Popup>
                  Координаты: {el?.latitude}, {el?.longitude} <br />
                  Скорость: {el?.speed} <br />
                  Запрет парковки: {noParking ? "да" : "нет"}
                </Popup>
              </Marker>
            ),
        )}
      {polygons &&
        polygons.map((polygon, index) => (
          <Polygon key={index} positions={polygon} color="blue" />
        ))}
      {polygons_ext &&
        polygons_ext.map((polygon, index) => (
          <Polygon key={index} positions={polygon} color="red" />
        ))}
      {/*<LoadingIndicator />*/}
      <MapUpdater coordinates={coordinates} />
    </MapContainer>
  );
};

export default MapComponent;
