import React from "react";

class UserOptionLink extends React.Component {
  constructor(props) {
    super(props);
    this.showLoginForm = this.showLoginForm.bind(this);
  }
  showLoginForm(e) {
    if (this.props.hideDivs) this.props.hideDivs();
    this.props.showDiv.map((label) => {
      var div = document.getElementById(label);
      if (div) {
        div.className = "active";
        div.scrollIntoView({behavior: "smooth", block: "start", inline: "start"});
      }
    });
  }
  render() {
    return (
        <button id={this.props.id} className="btn btn-fiubar border-radius-xlarge"
           type="button" onClick={this.showLoginForm}>{this.props.text}</button>
    );
  }
}

class UserOptions extends React.Component {
  hideDivs() {
    document.getElementById("elegir-carrera").className = "div-none";
    document.getElementById("elegir-materias").className = "div-none";
    document.getElementById("save-data").className = "div-none";
    document.getElementById("account-login").className = "div-none";
    document.getElementById("account-signup").className = "div-none";
  }
  render() {
    const newUserShowDivs = ['elegir-carrera'];
    const loginShowDivs = ['account-login'];
    return (
      <div id="user-options">
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

export { UserOptions, UserOptionLink };
