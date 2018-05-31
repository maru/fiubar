import React from "react";
import { UserOptionLink } from "./UserOptions";

class SaveData extends React.Component {

  // handleSubmit = e => {
  //   // <form onSubmit={this.handleSubmit}>
  //   e.preventDefault();
  //   const { name, email, message } = this.state;
  //   const lead = { name, email, message };
  //   const conf = {
  //     method: "post",
  //     body: JSON.stringify(lead),
  //     headers: new Headers({ "Content-Type": "application/json" })
  //   };
  //   fetch(this.props.endpoint, conf).then(response => console.log(response));
  // };
  hideDivs() {
    document.getElementById("account-login").className = "div-none";
    document.getElementById("account-signup").className = "div-none";
  }

  render() {
    const newUserShowDivs = ['account-signup'];
    const loginShowDivs = ['account-login'];
    const carrera = this.props.carrera;
    const plancarrera = this.props.plancarrera;
    const min_creditos = plancarrera ? plancarrera.min_creditos : 0;

    /* Calcular porcentaje de creditos */
    var creditos = 0;
    var materias = [];
    this.props.materias.forEach((materia, key) => {
      materias.push(materia);
      if (materia.estado == 'A')
        creditos += materia.creditos;
    });
    const radius = 25;
    const pieRadius = Math.round(2*Math.PI*radius);
    const creditosAng = Math.min(pieRadius, min_creditos > 0 ? Math.round(creditos * pieRadius / min_creditos) : 0);
    const creditosPerc = Math.min(100, min_creditos > 0 ? Math.round(creditos * 100 / min_creditos) : 0);

    return (
      <div id="save-data" className="div-none">
          <hr />
          <h2 className="">{plancarrera && plancarrera.name}</h2>
          <div id="carreraChart">
            <p className="lead">{creditosPerc}% de la carrera aprobada!</p>
            <svg width="100" height="100">
              <circle style={{ strokeDasharray: `${creditosAng} ${pieRadius}`}} r={radius} cx="50" cy="50" />
            </svg>
          </div>
          <p>Guardá tus cambios</p>
          <div className="container">
            <div className="row">
              <div className="col-sm">
                <UserOptionLink hideDivs={this.hideDivs} showDiv={newUserShowDivs} text="Nuevo usuario" id="new-user-link" /></div>
              <div className="link-or"> </div>
              <div className="col-sm">
                <UserOptionLink hideDivs={this.hideDivs} showDiv={loginShowDivs} text="Iniciar sesión" id="log-in-link" /></div>
            </div>
        </div>
      </div>
    );
  }
}
export default SaveData;
