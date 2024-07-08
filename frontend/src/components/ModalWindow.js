import { Modal } from "react-bootstrap";
import React from "react";
import { backend } from "../backend";

export default function ModalWindow({
  showModal,
  setShowModal,
  buildingInfo,
  setBuildingInfo,
}) {
  const testFn = async () => {
    if (buildingInfo?.id !== null) {
      const test = `${backend}accident_area?object_id=${buildingInfo?.id}`;
      const response = await fetch(test);
      const data = await response.json();
      const coords = data.nodes_rect.map(([lat, lng]) => [lat, lng]);
      const extended_area = data.nodes_rect_ext.map(([lat, lng]) => [lat, lng]);
      await setBuildingInfo((prevState) => ({
        ...prevState,
        coords,
        extended_area,
      }));
    }
    setShowModal(false);
  };
  return (
    <Modal show={showModal} onHide={() => setShowModal(false)}>
      <Modal.Header closeButton>
        <Modal.Title>Информация об аварии</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {buildingInfo && (
          <div>
            {buildingInfo?.id && <p>ID: {buildingInfo?.id}</p>}
            <p>
              Координаты: {buildingInfo?.latlng?.lat}{" "}
              {buildingInfo?.latlng?.lng}
            </p>
          </div>
        )}
      </Modal.Body>
      <Modal.Footer>
        <button className="btn btn-danger" onClick={testFn}>
          Подтвердить
        </button>
        <button
          className="btn btn-secondary"
          onClick={() => setShowModal(false)}
        >
          Закрыть
        </button>
      </Modal.Footer>
    </Modal>
  );
}
