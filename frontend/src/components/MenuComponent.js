import React, { useCallback } from "react";
import { backend } from "../backend";

const MenuComponent = ({ data, setState, objects, setObjects }) => {
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
  console.log(objects);

  const handleSelectChange = useCallback(
    (event) => {
      const { value } = event.target;
      console.log(event.target.value);
      switch (value) {
        case "all":
          setObjects((prevState) => ({
            ...prevState,
            count: data.length,
            data,
          }));
          break;
        case "savr":
          const notMobileUsers = data.filter(
            (el) => !el.hasOwnProperty("android_state"),
          );
          console.log(notMobileUsers);
          setObjects((prevState) => ({
            ...prevState,
            count: notMobileUsers.length,
            data: notMobileUsers,
          }));
          break;
        case "android_state":
          const mobileUsers = data.filter((el) =>
            el.hasOwnProperty("android_state"),
          );
          console.log(mobileUsers);
          setObjects((prevState) => ({
            ...prevState,
            count: mobileUsers.length,
            data: mobileUsers,
          }));
          break;
        default:
          setObjects((prevState) => ({
            ...prevState,
            count: data.length,
            data,
          }));
          break;
      }
    },
    [data, setObjects],
  );
  return (
    <>
      <select style={{margin:"1rem 0"}} className="form-select" defaultValue={"all"} onChange={handleSelectChange}>
        <option value="all">Все</option>
        <option value="savr">САВР</option>
        <option value="android_state">Мобильные пользователи</option>
      </select>
      <div>
        {data?.length ? (
          objects?.data?.map(
            (el, index) =>
              el?.latitude !== null &&
              el?.latitude !== "null" && (
                <div
                  key={index}
                  className="card border-dark mb-3 text-bg-light"
                  style={{ cursor: "pointer" }}
                  onClick={() => handleShow(el?.latitude, el?.longitude)}
                >
                  {/*<div className="card-header">*/}

                  {/*</div>*/}
                  <div className="card-body" style={{ textAlign: "left" }}>
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
                    <p className="card-title">Скорость: {el?.speed} км/ч</p>
                    {el.speed === "0" && (
                      <p className="card-title">
                        Парковка{" "}
                        {el?.parking === false ? "запрещена" : "не запрещена"}
                      </p>
                    )}
                    <p className="card-text">Последнее обновление: {el.datetime}</p>
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
    </>
  );
};

export default MenuComponent;
