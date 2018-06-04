import React from "react";
import ReactDOM from "react-dom";
import shortid from "shortid";

const uuid = shortid.generate;

class CarreraSelect extends React.Component {
  state = {
      data: [],
      isLoading: false,
      placeholder: "Cargando..."
  };

  constructor(props) {
    super(props);
    this.endpoint="api/facultad/carreras/";
  }

  componentDidMount() {
    this.fetchAPI(this.endpoint);
  }

  fetchAPI(url) {
    fetch(url)
      .then((response) => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then((data) => {
        this.setState({ data : data, isLoading: true });
      })
      .catch(error => this.setState({ placeholder: error, isLoading: false }));
  }

  handleCarreraClick(carrera, e) {
    this.props.onCarreraChange(carrera);
    document.getElementById("save-data").className = 'div-none';
  }

  render() {
    const { data, isLoading, placeholder } = this.state;

    if (!isLoading) return <p>{placeholder}</p>;

    return !data.length ? (
        <p>Error: no hay carreras.</p>
      ) : (
        <div className="container">
            <p className="lead text-left">Seleccioná una carrera:</p>
        {data.map(el => (
            <div className="box text-center" key={el.short_name}
                style={{ background: `linear-gradient(
                                        rgba(0, 0, 0, 0.5),
                                        rgba(0, 0, 0, 0.5)
                                      ), url(/static/images/facultad/carreras/${el.short_name}.jpg)
                                      no-repeat center center` }}
                onClick={(e) => this.handleCarreraClick(el, e)}>
                <div>{el.name}</div>
            </div>
        ))}
        </div>
      );
  }
}

class PlanCarreraSelect extends React.Component {
  state = {
      data: [],
      isLoading: false,
      placeholder: "Cargando...",
      selectedOption: 0
  };

  fetchAPI(carrera_id) {
    const url = "api/facultad/carreras/" + carrera_id + "/plancarreras/";

    fetch(url)
      .then((response) => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then((data) => {
        this.setState({ data : data, isLoading: true });
        if (data.length) {
          this.setState({ selectedOption : data[0].id });
          this.handlePlanCarreraClick(data[0], null);
        }
      })
      .catch(error => this.setState({ placeholder: error, isLoading: false }));
  }
  handlePlanCarreraClick(plancarrera, e) {
    this.setState({ selectedOption : plancarrera.id });
    this.props.onPlanCarreraChange(plancarrera);
    document.getElementById("elegir-materias").className = 'active';
    document.getElementById("save-data").className = 'div-none';
  }
  render() {
    const { data, isLoading, placeholder } = this.state;

    if (!isLoading) return <p>{placeholder}</p>;

    return !data.length ? (
      <p>No hay planes para {this.props.carrera.name}</p>
      ) : (
        <div className="container text-left">
        <p className="lead">Elegí el plan:</p>
          <form>
          {data.map(el => (
            <div className="form-check" key={uuid()}>
              <input className="form-check-input" type="radio" name="plancarrera"
                  id={`plancarrera${el.id}`}
                  value={el.id}
                  checked={this.state.selectedOption === el.id}
                  onChange={(e) => this.handlePlanCarreraClick(el, e)}
                />
                <label className="form-check-label" htmlFor={`plancarrera${el.id}`}>
                {el.name}
                </label>
              </div>
          ))}
          </form>
        </div>
      );
  }
}

class ElegirCarrera extends React.Component {
  constructor(props) {
    super(props);
    this.handleCarreraChange = this.handleCarreraChange.bind(this);
    this.handlePlanCarreraChange = this.handlePlanCarreraChange.bind(this);
    this.planCarrera = React.createRef();
  }

  handleCarreraChange(carrera) {
    document.getElementById("save-data").className = 'div-none';
    this.props.onCarreraChange(carrera);
    if (carrera == null || carrera.id < 0) return;
    this.planCarrera.current.fetchAPI(carrera.id);
    document.getElementById("elegir-carrera-plan").className = 'active';
  }

  handlePlanCarreraChange(plancarrera) {
    this.props.onPlanCarreraChange(plancarrera);
  }

  render() {
    return (
      <div id="elegir-carrera" className="collapse">
        <hr />
        <h2 className="">¿Qué carrera cursás?</h2>
        <div id="carreras-list">
            <CarreraSelect
                carrera={this.props.carrera}
                onCarreraChange={this.handleCarreraChange}
              />
        </div>
        <div id="elegir-carrera-plan" className="div-none">
            <PlanCarreraSelect
                ref={this.planCarrera}
                carrera={this.props.carrera}
                plancarrera={this.props.plancarrera}
                onPlanCarreraChange={this.handlePlanCarreraChange}
              />
        </div>
      </div>
    );
  }
}


export default ElegirCarrera;
