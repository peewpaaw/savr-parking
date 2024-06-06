import React from "react";

const MenuComponent = ({ data, setState }) => {
  const handleShow = async (latitude, longitude) => {
    if (!isNaN(latitude) && !isNaN(longitude)) {
      const response = await fetch(
        `http://127.0.0.1:8000/nearest?lat=${latitude}&lon=${longitude}`,
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
      <div className="card">
        <div className="card-body">
          {data?.map(
            (el) =>
              el?.latitude !== null &&
              el?.latitude !== "null" && (
                <p style={{cursor:'pointer'}} onClick={() => handleShow(el?.latitude, el?.longitude)}>
                  {el?.object_name}
                </p>
              ),
          )}
        </div>
      </div>
    </div>
  );
};

export default MenuComponent;
