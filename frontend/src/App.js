// import logo from './logo.svg';
// import './App.css';
// import Map from './Map';

// function App() {
//   return (
//     <div className="App">
//       <Map/>
//     </div>
//   );
// }

// export default App;

// src/App.js
import React, { useState } from 'react';
import './App.css';
import MapComponent from './MapComponent';
import MenuComponent from './MenuComponent';

function App() {
  const [state, setState] = useState({ coordinates: { lat: 51.505, lng: -0.09 }, polygons: [], polygons_ext: [], noParking: false});

  const handleShow = ({ coordinates, polygons, polygons_ext, noParking }) => {
    setState({ coordinates, polygons, polygons_ext, noParking });
  };

  return (
    <div className="App">
      <div className="menu">
        <MenuComponent onShow={handleShow} />
      </div>
      <div className="map">
        <MapComponent coordinates={state.coordinates} polygons={state.polygons} polygons_ext={state.polygons_ext} noParking={state.noParking} />
      </div>
    </div>
  );
}

export default App;


