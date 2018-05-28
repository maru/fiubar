import React from "react";
import ReactDOM from "react-dom";
import PageTitle from "./PageTitle";
import ElegirCarrera from "./ElegirCarrera";
import ElegirMaterias from "./ElegirMaterias";
import { UserOptions, SaveData } from "./UserOptions";
import { AccountLoginForm, AccountSignupForm } from "./AccountForm";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      carrera: 'not set',
      materiasAprobadas: [],
      materiasFinal: [],
      materiasCursando: []
    };

    this.handleCarreraChange = this.handleCarreraChange.bind(this);
    this.handleMateriasAprobadasChange = this.handleMateriasAprobadasChange.bind(this);
    this.handleMateriasFinalChange = this.handleMateriasFinalChange.bind(this);
    this.handleMateriasCursandoChange = this.handleMateriasCursandoChange.bind(this);
  }

  handleCarreraChange(carrera) {
    this.setState({
      carrera: carrera
    });
  }

  handleMateriasAprobadasChange(materiasAprobadas) {
    this.setState({
      materiasAprobadas: materiasAprobadas
    });
  }

  handleMateriasFinalChange(materiasFinal) {
    this.setState({
      materiasFinal: materiasFinal
    });
  }

  handleMateriasCursandoChange(materiasCursando) {
    this.setState({
      materiasCursando: materiasCursando
    });
  }

  render() {
    return (
      <React.Fragment>
        <PageTitle />
        <UserOptions />
        <ElegirCarrera
          carrera={this.state.carrera}
          onCarreraChange={this.handleCarreraChange}
        />
        <ElegirMaterias
          carrera={this.state.carrera}
          materiasAprobadas={this.state.materiasAprobadas}
          materiasFinal={this.state.materiasFinal}
          materiasCursando={this.state.materiasCursando}
        />
        <SaveData
          carrera={this.state.carrera}
        />
      </React.Fragment>
    );
  }
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
