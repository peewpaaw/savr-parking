import { Offcanvas } from "react-bootstrap";
import React, { useState } from "react";

export default function OffcanvasComponent({ title, children }) {
  const [show, setShow] = useState(true);
  const handleClose = () => setShow(false);
  const toggleShow = () => setShow((s) => !s);

  return (
    <>
      <button onClick={toggleShow} className="btn">
        <img
          style={{ width: "36px" }}
          alt={"menu"}
          src={require("../assign/menu.png")}
        />
      </button>
      <Offcanvas
        backdrop={false}
        scroll={true}
        show={show}
        style={{ backgroundColor: "#f8f9fa" }}
        onHide={handleClose}
      >
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>{title}</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>{children}</Offcanvas.Body>
      </Offcanvas>
    </>
  );
}
