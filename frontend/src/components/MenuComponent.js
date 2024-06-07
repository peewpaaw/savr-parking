import React from "react";
import { backend } from "../backend";

const MenuComponent = ({ data, setState }) => {
  const handleShow = async (latitude, longitude) => {
    if (!isNaN(latitude) && !isNaN(longitude)) {
      const response = await fetch(
        `${backend}nearest?lat=${latitude}&lon=${longitude}`,
      );
      const data = await response.json();

      const polygons = data.map((polygon) =>
        polygon.nodes_rect.map(([lat, lng]) => [lat, lng]),
      );
      const polygons_ext = data.map((polygon_ext) =>
        polygon_ext.nodes_rect_ext.map(([lat, lng]) => [lat, lng]),
      );
      const noParking = data.some((item) => item.parking === false);

      setState({
        coordinates: { lat: latitude, lng: longitude },
        polygons,
        polygons_ext,
        noParking,
      });
    }
  };

  return (
    <div style={{ padding: "10px" }}>
      <h5>Список транспортных средств</h5>
      <div>
        {data?.length ? (
          data?.map(
            (el) =>
              el?.latitude !== null &&
              el?.latitude !== "null" && (
                <div
                  className="card border-dark mb-3"
                  style={{ cursor: "pointer" }}
                  onClick={() => handleShow(el?.latitude, el?.longitude)}
                >
                  <div className="card-header">
                    <div
                      className={
                        el?.speed > 0
                          ? " circle speed"
                          : el.parking === true
                            ? "circle parking"
                            : "circle no-parking"
                      }
                    >
                      <h5>{el?.object_name}</h5>
                    </div>
                  </div>
                  <div className="card-body" style={{textAlign:'left'}}>
                    <p className="card-title">Скорость: {el?.speed} км/ч</p>
                    {el.speed === '0' && (
                      <p className="card-text">
                        Парковка{" "}
                        {el?.parking === false ? "запрещена" : "не запрещена"}
                      </p>
                    )}
                    <p>Последнее обновление: {el.datetime}</p>
                  </div>
                </div>
              ),
          )
        ) : (
          <div className="spinner-border" role="status">
            <span className="sr-only" />
          </div>
        )}
      </div>
    </div>
  );
};

export default MenuComponent;
