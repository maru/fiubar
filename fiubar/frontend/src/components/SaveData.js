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

    return (
      <div id="save-data" className="div-none">
          <hr style={{ border: 0 }}/>
          <div className="container">
            <div className="row">
              <div className="col">
                <UserOptionLink hideDivs={this.hideDivs} showDiv={newUserShowDivs} text="Nuevo usuario" id="new-user-link" /></div>
              <div className="col">
                <UserOptionLink hideDivs={this.hideDivs} showDiv={loginShowDivs} text="Iniciar sesión" id="log-in-link" /></div>
            </div>
        </div>
      </div>
    );
  }
}
export default SaveData;
