import React, { useState, useEffect } from 'react';
import { ListGroup, FormControl } from 'react-bootstrap';

const VehicleListComponent = () => {
  const [vehicles, setVehicles] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchVehicles = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/vehicles');
        const data = await response.json();
        setVehicles(data);
      } catch (error) {
        console.error('Error fetching vehicles:', error);
      }
    };

    fetchVehicles();
  }, []);

  const filteredVehicles = vehicles.filter(vehicle =>
    vehicle.name && vehicle.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vehicle.auto_number && vehicle.auto_number.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ marginTop: '20px' }}>
      <h5>Список Транспорта</h5>
      <FormControl
        type="text"
        placeholder="Поиск по имени"
        className="mb-3"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <ListGroup>
        {filteredVehicles.map((vehicle) => (
          <ListGroup.Item key={vehicle.object_id}>
            {vehicle.name} 
            {/* - {vehicle.auto_number || 'Без номера'} */}
          </ListGroup.Item>
        ))}
      </ListGroup>
    </div>
  );
};

export default VehicleListComponent;
