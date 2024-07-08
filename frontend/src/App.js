import React, { useEffect, useState } from "react";
import "./App.css";
import MapComponent from "./components/MapComponent";
import MenuComponent from "./components/MenuComponent";
import axios from "axios";
import { backend } from "./backend";
import OffcanvasComponent from "./components/Offcanvas";

function App() {
  const [state, setState] = useState({
    coordinates: { lat: 53.9023, lng: 27.5619 },
    polygons: [],
    polygons_ext: [],
    noParking: false,
  });
  const vehicles = `${backend}vehicles_position`;
  const users = `${backend}persons_position`;
  const [data, setData] = useState([]);
  const [usersData, setUsersData] = useState([]);
  const [typeInfo, setTypeInfo] = useState("");
  const fetchData = async () => {
    try {
      const response = await axios.get(vehicles);
      setData(response.data);
    } catch (error) {
      console.log(error);
    }
  };
  const fetchUsersData = async () => {
    try {
      const response = await axios.get(users);
      setUsersData(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      fetchData().then((r) => console.log(r));
      fetchUsersData().then((r) => console.log(r));
    }, 7000);
    return () => clearInterval(interval);
  }, [fetchData, fetchUsersData]);

  return (
    <div className="App">
      <OffcanvasComponent
        title={`Список объектов: ${typeInfo === "" || typeInfo === "all" ? data.length + usersData.length : typeInfo === "savr" ? data.length : usersData.length}`}
        children={
          <MenuComponent
            data={data}
            setState={setState}
            usersData={usersData}
            typeInfo={typeInfo}
            setTypeInfo={setTypeInfo}
          />
        }
      />
      <div className="map">
        <MapComponent
          data={data}
          coordinates={state.coordinates}
          polygons={state.polygons}
          polygons_ext={state.polygons_ext}
          noParking={state.noParking}
          setState={setState}
          typeInfo={typeInfo}
          usersData={usersData}
        />
      </div>
    </div>
  );
}

export default App;
