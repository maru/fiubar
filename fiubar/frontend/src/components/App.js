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

    this.saveData = this.saveData.bind(this);
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
  }

  handlePlanCarreraChange(plancarrera) {
    this.setState({
      plancarrera: plancarrera
    });
    this.materiasDiv.current.fetchAPI(plancarrera.id);
  }
  handleMateriasChange(materias) {
    this.setState({
      materias: materias
    });
  }
  /* Save data in cookies */
  saveData() {
    const { carrera, plancarrera, materias } = this.state;
    document.cookie = "create_alumno=1";
    document.cookie = "carrera" + "=" + JSON.stringify(carrera);
    document.cookie = "plancarrera" + "=" + JSON.stringify(plancarrera);
    document.cookie = "materias" + "=" + JSON.stringify([...materias]);
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
          saveData={this.saveData}
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
