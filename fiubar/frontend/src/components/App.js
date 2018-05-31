import React from "react";
import ReactDOM from "react-dom";
import PageTitle from "./PageTitle";
import ElegirCarrera from "./ElegirCarrera";
import ElegirMaterias from "./ElegirMaterias";
import { UserOptions } from "./UserOptions";
import SaveData from "./SaveData";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      carrera: null,
      plancarrera: null,
      materias: new Map()
    };

    this.handleCarreraChange = this.handleCarreraChange.bind(this);
    this.handlePlanCarreraChange = this.handlePlanCarreraChange.bind(this);
    this.handleMateriasChange = this.handleMateriasChange.bind(this);

    this.materiasDiv = React.createRef();
  }

  handleCarreraChange(carrera) {
    this.setState({
      carrera: carrera,
      plancarrera: -1
    });
    sessionStorage.setItem('carrera', JSON.stringify(carrera));
  }

  handlePlanCarreraChange(plancarrera) {
    this.setState({
      plancarrera: plancarrera
    });
    this.materiasDiv.current.fetchAPI(plancarrera.id);
    sessionStorage.setItem('plancarrera', JSON.stringify(plancarrera));
  }
  handleMateriasChange(materias) {
    this.setState({
      materias: materias
    });
    sessionStorage.setItem('materias', JSON.stringify(materias));
  }

  render() {
    return (
      <React.Fragment>
        <PageTitle />
        <UserOptions />
        <ElegirCarrera
          carrera={this.state.carrera}
          plancarrera={this.state.plancarrera}
          onCarreraChange={this.handleCarreraChange}
          onPlanCarreraChange={this.handlePlanCarreraChange}
        />
        <ElegirMaterias
          ref={this.materiasDiv}
          carrera={this.state.carrera}
          plancarrera={this.state.plancarrera}
          materias={this.state.materias}
          onMateriasChange={this.handleMateriasChange}
        />
        <SaveData
          carrera={this.state.carrera}
          plancarrera={this.state.plancarrera}
          materias={this.state.materias}
        />
      </React.Fragment>
    );
  }
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
