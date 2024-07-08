import { Popup } from "react-leaflet";
import React from "react";

export default function PopupComponent({ loader, el, noParking }) {
  return (
    <Popup>
      {loader ? (
        <p>Загрузка...</p>
      ) : (
        <>
          Объект: {el.object_name} <br />
          Координаты: {el?.latitude}, {el?.longitude} <br />
          {el.android_state ? (
            <></>
          ) : (
            <>
              Скорость: {el?.speed} <br />
              Запрет парковки: {noParking ? "да" : "нет"}
            </>
          )}
        </>
      )}
    </Popup>
  );
}
