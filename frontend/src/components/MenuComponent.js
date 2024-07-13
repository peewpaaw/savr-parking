import React, { useCallback } from "react";
import { backend } from "../backend";

const MenuComponent = ({
  data,
  setState,
  usersData,
  typeInfo,
  setTypeInfo,
}) => {
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

      await setState({
        coordinates: { lat: latitude, lng: longitude },
        polygons,
        polygons_ext,
        noParking,
      });
    }
  };

  const handleSelectChange = useCallback(
    (event) => {
      const { value } = event.target;
      setTypeInfo(value);
    },
    [setTypeInfo],
  );

  return (
    <>
      <select
        style={{ margin: "1rem 0" }}
        className="form-select"
        defaultValue={"all"}
        onChange={handleSelectChange}
      >
        <option value="all">Все</option>
        <option value="savr">САВР</option>
        <option value="android_state">Мобильные пользователи</option>
      </select>
      <div>
        {data?.length ? (
          <>
            {(typeInfo === "all" || typeInfo === "savr" || typeInfo === "") &&
              data?.map(
                (el, index) =>
                  el?.latitude !== null &&
                  el?.latitude !== "null" && (
                    <div
                      key={index}
                      className="card mb-3"
                      style={{ cursor: "pointer" }}
                      onClick={() => handleShow(el?.latitude, el?.longitude)}
                    >
                      <div
                        className="card-body"
                        style={{
                          textAlign: "left",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "space-between",
                        }}
                      >
                        <div>
                          <div
                            className={
                              el?.speed > 0
                                ? "circle speed"
                                : el.parking === true
                                  ? "circle parking"
                                  : "circle no-parking"
                            }
                          >
                            <h4>{el?.object_name}</h4>
                          </div>
                          <p className="card-title">{el?.speed} км/ч</p>
                        </div>
                        <div>
                          <img alt={"car"} src={require("../assign/car.png")} />
                        </div>
                      </div>
                    </div>
                  ),
              )}
            {(typeInfo === "all" ||
              typeInfo === "android_state" ||
              typeInfo === "") &&
              usersData?.map(
                (el, index) =>
                  el?.latitude !== null &&
                  el?.latitude !== "null" && (
                    <div
                      key={index}
                      className="card mb-3"
                      style={{ cursor: "pointer" }}
                      onClick={() =>
                        setState((prevState) => ({
                          ...prevState,
                          coordinates: {
                            lat: el?.latitude,
                            lng: el?.longitude,
                          },
                          polygons: [],
                          polygons_ext: [],
                          noParking: false,
                        }))
                      }
                    >
                      <div
                        className="card-body"
                        style={{
                          textAlign: "left",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "space-between",
                        }}
                      >
                        <div>
                          <div
                            className={
                              el?.speed > 0
                                ? " circle speed"
                                : el.parking === true
                                  ? "circle parking"
                                  : "circle no-parking"
                            }
                          >
                            <h4>{el?.object_name}</h4>
                          </div>
                          <p className="card-title">{el?.speed} км/ч</p>
                        </div>
                        <div>
                          <img alt={"users"} src={require("../assign/user.png")} />
                        </div>
                      </div>
                    </div>
                  ),
              )}
          </>
        ) : (
          <div className="spinner-border" role="status">
            <span className="sr-only" />
          </div>
        )}
      </div>
    </>
  );
};

export default MenuComponent;
