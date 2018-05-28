import React from "react";

class UserOptionLink extends React.Component {
  constructor(props) {
    super(props);
    this.showLoginForm = this.showLoginForm.bind(this);
  }
  showLoginForm(e) {
    document.getElementById("user-options").className = "d-none";
    document.getElementById("elegir-carrera").className = "d-none";
    document.getElementById("elegir-materias").className = "d-none";
    document.getElementById("save-data").className = "d-none";
    document.getElementById("account-login").className = "d-none";
    document.getElementById("account-signup").className = "d-none";

    this.props.showDiv.map((label) => {
      document.getElementById(label).className = "active";
      // if (label == 'elegir-carrera') {
      //   var heading = document.getElementById('head-title');
      //   if ((heading != null) && (heading.childElementCount >= 2)) {
      //     heading.children[0].style.fontSize = '25px';
      //     heading.children[1].style.fontSize = '14px';
      //   }
      // }
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
            <div className="col-sm link-or"></div>
            <div className="col-sm"><UserOptionLink showDiv={loginShowDivs} text="Iniciar sesión" id="log-in-link" /></div>
          </div>
        </div>
      </div>
    );
  }
}

class SaveData extends React.Component {
  render() {
    const newUserShowDivs = ['account-signup', 'save-data'];
    const loginShowDivs = ['account-login', 'save-data'];
    const carrera = this.props.carrera;
    return (
      <div id="save-data" className="d-none">
        <div className="container">
          <h2 className="">{carrera}</h2>
          <div>Guardá tus cambios</div>
          <div className="row">
          <div className="col-sm"><UserOptionLink showDiv={newUserShowDivs} text="Nuevo usuario" id="new-user-link" /></div>
          <div className="col-sm link-or"></div>
          <div className="col-sm"><UserOptionLink showDiv={loginShowDivs} text="Iniciar sesión" id="log-in-link" /></div>
          </div>
        </div>
      </div>
    );
  }
}

export { UserOptions, SaveData };
