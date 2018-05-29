import React from "react";

class UserOptionLink extends React.Component {
  constructor(props) {
    super(props);
    this.showLoginForm = this.showLoginForm.bind(this);
  }
  showLoginForm(e) {
    document.getElementById("account-login").className = "d-none";
    document.getElementById("account-signup").className = "d-none";

    this.props.showDiv.map((label) => {
      document.getElementById(label).className = "active";
    });
  }
  render() {
    return (
        <a href="#" id={this.props.id} className="btn btn-fiubar border-radius-xlarge"
           onClick={this.showLoginForm}>{this.props.text}</a>
    );
  }
}

class UserOptions extends React.Component {
  render() {
    const newUserShowDivs = ['elegir-carrera'];
    const loginShowDivs = ['account-login'];
    return (
      <div id="user-options">
        <div className="container">
          <div className="row">
            <div className="col-sm"><UserOptionLink showDiv={newUserShowDivs} text="Nuevo usuario" id="new-user-link" /></div>
            <div className="link-or"></div>
            <div className="col-sm"><UserOptionLink showDiv={loginShowDivs} text="Iniciar sesión" id="log-in-link" /></div>
          </div>
        </div>
      </div>
    );
  }
}

class SaveData extends React.Component {
  render() {
    const newUserShowDivs = ['account-signup'];
    const loginShowDivs = ['account-login'];
    const carrera = this.props.carrera;
    const plancarrera = this.props.plancarrera;
    return (
      <div id="save-data" className="d-none">
          <h2 className="">{plancarrera.name}</h2>
          <p>Guardá tus cambios</p>
          <div className="container">
            <div className="row">
              <div className="col-sm"><UserOptionLink showDiv={newUserShowDivs} text="Nuevo usuario" id="new-user-link" /></div>
              <div className="link-or"> </div>
              <div className="col-sm"><UserOptionLink showDiv={loginShowDivs} text="Iniciar sesión" id="log-in-link" /></div>
            </div>
        </div>
      </div>
    );
  }
}

export { UserOptions, SaveData };
