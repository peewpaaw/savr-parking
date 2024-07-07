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
  const query = `${backend}current_position`;
  const [data, setData] = useState([]);
  const [objects, setObjects] = useState({ count: null, data: [] });
  const fetchData = async () => {
    try {
      const response = await axios.get(query);
      setData(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      fetchData().then((r) => console.log(r));
    }, 7000);
    return () => clearInterval(interval);
  }, [fetchData]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(query);
        setObjects((prevState) => ({
          ...prevState,
          count: response.data.length,
          data: response.data,
        }));
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [query]);

  return (
    <div className="App">
      <OffcanvasComponent
        title={`Список объектов: ${objects.count}`}
        children={
          <MenuComponent
            data={data}
            setState={setState}
            setObjects={setObjects}
            objects={objects}
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
          objects={objects}
        />
      </div>
    </div>
  );
}

export default App;
