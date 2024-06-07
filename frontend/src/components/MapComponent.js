import React, { useEffect, useState } from "react";
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
import { backend } from "../backend";

const customIconParking = L.icon({
  iconUrl: require("../transportGreen.png"),
  iconSize: [42, 42],
  iconAnchor: [21, 42],
});
const customIconSpeed = L.icon({
  iconUrl: require("../transport.png"),
  iconSize: [42, 42],
  iconAnchor: [21, 42],
});
const customIconNotParking = L.icon({
  iconUrl: require("../transportRed.png"),
  iconSize: [42, 42],
  iconAnchor: [21, 42],
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
      map.flyTo([coordinates.lat, coordinates.lng], map.getZoom(12));
    }, [coordinates, map]);

    return null;
  };
  const [loader, setLoader] = useState(true);
  const handleMarkerClick = async (e) => {
    const response = await fetch(
      `${backend}nearest?lat=${e.latlng?.lat}&lon=${e.latlng?.lng}`,
    ).finally(() => {
      setLoader(false);
    });
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
      zoom={18}
      maxZoom={20}
      minZoom={7}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        maxZoom="20"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {data?.length &&
        data?.map(
          (el) =>
            el?.latitude && (
              <Marker
                icon={
                  el?.speed > 0
                    ? customIconSpeed
                    : el.parking === true
                      ? customIconParking
                      : customIconNotParking
                }
                eventHandlers={{ click: handleMarkerClick }}
                position={[el?.latitude, el?.longitude]}
              >
                <Popup>
                  {loader ? (
                    <p>Загрузка...</p>
                  ) : (
                    <>
                      Координаты: {el?.latitude}, {el?.longitude} <br />
                      Скорость: {el?.speed} <br />
                      Запрет парковки: {noParking ? "да" : "нет"}
                    </>
                  )}
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
      <MapUpdater coordinates={coordinates} />
    </MapContainer>
  );
};

export default MapComponent;
