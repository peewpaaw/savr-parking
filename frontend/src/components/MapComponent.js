import React, { useEffect, useState } from "react";
import {
  MapContainer,
  Marker,
  Polygon,
  Popup,
  TileLayer,
  useMap,
  useMapEvent,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { backend } from "../backend";
import { Button, Modal } from "react-bootstrap";

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

const locationIcon = L.icon({
  iconUrl: require("../location.png"),
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
  objects,
}) => {
  const [showModal, setShowModal] = useState(false);
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

  const [buildingInfo, setBuildingInfo] = useState(null);

  const handleMapClick = async (e) => {
    const { lat, lng } = e.latlng;
    console.log(e);
    // Формирование запроса к API Overpass для получения данных о зданиях
    const query = `
      [out:json];
      (
        way["building"](around:10, ${lat}, ${lng});
      );
      out body;
      >;
      out skel qt;
    `;

    const url = `https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`;

    try {
      const response = await fetch(url);
      const data = await response.json();

      // Ищем первый элемент типа "way"
      const buildingWay = data.elements.find(
        (element) => element.type === "way",
      );
      console.log(buildingWay);
      const buildingData = {
        id: buildingWay ? buildingWay.id : null,
        latlng: e.latlng,
      };
      setBuildingInfo(buildingData);
      setShowModal(true);
    } catch (error) {
      console.error("Ошибка при выполнении запроса к API Overpass:", error);
    }
  };

  // Хук для обработки кликов на карте
  const MapClickHandler = () => {
    useMapEvent("click", handleMapClick);
    return null;
  };
  console.log(buildingInfo?.latlng.lat);
  return (
    <>
      <MapContainer
        center={[coordinates?.lat, coordinates?.lng]}
        zoom={14}
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
            (el, index) =>
              el?.latitude && (
                <Marker
                  key={index}
                  icon={
                    el.android_state
                      ? locationIcon
                      : el?.speed > 0
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
                        Объект: {el.object_name} <br />
                        Координаты: {el?.latitude}, {el?.longitude} <br />
                        {el.android_state ? (
                          <></>
                        ) : (
                          <>
                            Скорость: {el?.speed} <br />
                            Запрет парковки: {noParking ? "да" : "нет"}
                          </>
                        )}
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
        <MapClickHandler />
      </MapContainer>
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Информация об аварии</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {buildingInfo && (
            <div>
              {buildingInfo?.id && <p>ID: {buildingInfo?.id}</p>}
              <p>
                Координаты: {buildingInfo?.latlng?.lat}{" "}
                {buildingInfo?.latlng?.lng}
              </p>
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <button className="btn btn-danger" onClick={() => setShowModal(false)}>
            Подтвердить
          </button>
          <button className="btn btn-secondary" onClick={() => setShowModal(false)}>
            Закрыть
          </button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default MapComponent;
