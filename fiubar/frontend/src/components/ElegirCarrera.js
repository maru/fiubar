import React, { Component } from "react";
import PropTypes from "prop-types";
import Table from "./Table.js";

class DataProvider extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired
  };
  state = {
      data: [],
      loaded: false,
      placeholder: "Loading..."
    };
  componentDidMount() {
    fetch(this.props.endpoint)
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then(data => this.setState({ data: data, loaded: true }));
  }
  render() {
    const { data, loaded, placeholder } = this.state;
    return loaded ? this.props.render(data) : <p>{placeholder}</p>;
  }
}

class ElegirCarrera extends React.Component {
  constructor(props) {
    super(props);
    this.handleCarreraChange = this.handleCarreraChange.bind(this);
  }

  handleCarreraChange(e) {
    this.props.onCarreraChange(e.target.value);
  }

  handlePlanCarreraChange(e) {
    this.props.onCarreraChange(e.target.value);
  }


  render() {
    return (
      <div id="elegir-carrera" className="d-none">
        <h2 className="">¿Qué carrera cursás?</h2>
        <div id="carreras-list">
            <DataProvider endpoint="api/facultad/carreras/"
                          render={data => <Table data={data} />} />
        </div>

        <div id="elegir-carrera-plan" className="d-none">
          <h2 className="">Elegí el plan</h2>
        </div>

        <div id="elegir-carrera-plan-orientacion" className="d-none">
          <h2 className="">Elegí la orientación</h2>
        </div>
      </div>
    );
  }
}
export default ElegirCarrera;
