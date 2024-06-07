import React, { useEffect, useState } from "react";
import "./App.css";
import MapComponent from "./components/MapComponent";
import MenuComponent from "./components/MenuComponent";
import axios from "axios";
import { backend } from "./backend";

function App() {
  const [state, setState] = useState({
    coordinates: { lat: 53.900479, lng: 27.558558 },
    polygons: [],
    polygons_ext: [],
    noParking: false,
  });
  const query = `${backend}current_position`;
  const [data, setData] = useState([]);

  useEffect(() => {
    axios(query)
      .then((res) => setData(res.data))
      .catch((error) => console.log(error));
  }, [query]);

  return (
    <div className="App">
      <div className="menu">
        <MenuComponent data={data} setState={setState} />
      </div>
      <div className="map">
        <MapComponent
          data={data}
          coordinates={state.coordinates}
          polygons={state.polygons}
          polygons_ext={state.polygons_ext}
          noParking={state.noParking}
          setState={setState}
        />
      </div>
    </div>
  );
}

export default App;
