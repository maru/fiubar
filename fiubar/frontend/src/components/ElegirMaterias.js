import React from "react";

class ElegirMaterias extends React.Component {
  render() {
    return (
      <div id="elegir-materias" className="d-none">
        <div id="elegir-materias-title-aprobadas" className="">
          <h2 className="">¿Qué materias aprobaste?</h2>
        </div>
        <div id="elegir-materias-title-final" className="">
          <h2 className="">¿Qué materias debés final?</h2>
        </div>
        <div id="elegir-materias-title-cursando" className="">
          <h2 className="">¿Qué materias estás cursando?</h2>
        </div>
      </div>
    );
  }
}
export default ElegirMaterias;
