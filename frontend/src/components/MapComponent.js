import React, { useEffect, useState } from "react";
import {
  Circle,
  MapContainer,
  Marker,
  Polygon,
  TileLayer,
  useMap,
  useMapEvent,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { backend } from "../backend";
import ModalWindow from "./ModalWindow";
import PopupComponent from "./Popup";

const customIconParking = L.icon({
  iconUrl: require("../assign/vanGreen.png"),
  iconSize: [42, 42],
  iconAnchor: [21, 42],
});
const customIconSpeed = L.icon({
  iconUrl: require("../assign/van.png"),
  iconSize: [42, 42],
  iconAnchor: [21, 42],
});
const customIconNotParking = L.icon({
  iconUrl: require("../assign/varRed.png"),
  iconSize: [42, 42],
  iconAnchor: [21, 42],
});

const locationIcon = L.icon({
  iconUrl: require("../assign/circle.png"),
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
  typeInfo,
  usersData,
}) => {
  const [showModal, setShowModal] = useState(false);
  const [buildingInfo, setBuildingInfo] = useState(null);
  const MapUpdater = ({ coordinates }) => {
    const map = useMap();

    useEffect(() => {
      map.flyTo([coordinates.lat, coordinates.lng], map.getZoom(14));
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

  const handleMapClick = async (e) => {
    const { lat, lng } = e.latlng;
    await setState((prevState) => ({
      ...prevState,
      coordinates: { lat, lng },
      polygons: [],
      polygons_ext: [],
      noParking: false,
    }));
    // // Формирование запроса к API Overpass для получения данных о зданиях
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

      const buildingData = {
        id: buildingWay?.id ? buildingWay?.id : null,
        latlng: e.latlng,
        center: [lat, lng],
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
        {buildingInfo &&
          (buildingInfo?.coords ? (
            <>
              <Polygon positions={buildingInfo?.coords} color="blue" />
              <Polygon positions={buildingInfo?.extended_area} color="red" />
            </>
          ) : (
            <Circle center={buildingInfo?.center} radius={50} color="red" />
          ))}
        {(typeInfo === "" || typeInfo === "all" || typeInfo === "savr") &&
          data?.length &&
          data?.map(
            (el, index) =>
              el?.latitude && (
                <Marker
                  key={index}
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
                  <PopupComponent
                    el={el}
                    loader={loader}
                    noParking={noParking}
                  />
                </Marker>
              ),
          )}
        {(typeInfo === "" ||
          typeInfo === "all" ||
          typeInfo === "android_state") &&
          usersData?.length &&
          usersData?.map(
            (el, index) =>
              el?.latitude && (
                <Marker
                  key={index}
                  icon={locationIcon}
                  eventHandlers={{
                    click: (e) => {
                      setState({
                        coordinates: { lat: e.latlng?.lat, lng: e.latlng?.lng },
                        polygons: null,
                        polygons_ext: null,
                        noParking: null,
                      });
                      setLoader(false);
                    },
                  }}
                  position={[el?.latitude, el?.longitude]}
                >
                  <PopupComponent
                    el={el}
                    loader={loader}
                    noParking={noParking}
                  />
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
      <ModalWindow
        setBuildingInfo={setBuildingInfo}
        showModal={showModal}
        setShowModal={setShowModal}
        buildingInfo={buildingInfo}
      />
    </>
  );
};

export default MapComponent;
