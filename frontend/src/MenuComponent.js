// src/MenuComponent.js
import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import VehicleListComponent from './VehicleListComponent';

const MenuComponent = ({ onShow }) => {
  const [lat, setLat] = useState('');
  const [lng, setLng] = useState('');

  const handleShow = async () => {
    const latitude = parseFloat(lat);
    const longitude = parseFloat(lng);
    if (!isNaN(latitude) && !isNaN(longitude)) {
      const response = await fetch(`http://127.0.0.1:8000/nearest?lat=${latitude}&lon=${longitude}`);
      const data = await response.json();

      const polygons = data.map(polygon => polygon.nodes_rect.map(([lat, lng]) => [lat, lng]));
      const polygons_ext = data.map(polygon_ext => polygon_ext.nodes_rect_ext.map(([lat, lng]) => [lat, lng]));
      const noParking = data.some(item => item.parking === false)
      console.log("np parking:")
      console.log(noParking)      

      onShow({ coordinates: { lat: latitude, lng: longitude }, polygons, polygons_ext, noParking });
    }
  };

  return (
    <div style={{ padding: '10px' }}>
        <h5>Координаты точки</h5>
      <div class="card">
        <div class="card-body">
          <Form>
            <Form.Group controlId="formLatitude">
              <Form.Label>Широта</Form.Label>
              <Form.Control
                type="text"
                value={lat}
                onChange={(e) => setLat(e.target.value)}
                placeholder="Введите широту"
              />
            </Form.Group>
            <Form.Group controlId="formLongitude">
              <Form.Label>Долгота</Form.Label>
              <Form.Control
                type="text"
                value={lng}
                onChange={(e) => setLng(e.target.value)}
                placeholder="Введите долготу"
              />
            </Form.Group>
            <Button variant="primary" onClick={handleShow} style={{ marginTop: '10px' }}>
              Показать
            </Button>
          </Form>
        </div>
      </div>
      <br></br>
      <div class="alert alert-primary">Область здания</div>
      <div class="alert alert-danger">Область запрета парковки</div>
      {/* <VehicleListComponent /> */}
    </div>
  );
};

export default MenuComponent;
