import React from "react";
import shortid from "shortid";

const uuid = shortid.generate;

/* Calcular porcentaje de creditos */
class CreditosChart extends React.Component {
  render() {
    const creditos = this.props.creditos;
    const min_creditos = this.props.min_creditos;
    const radius = 25;
    const pieRadius = Math.round(2*Math.PI*radius);
    const creditosAng = Math.min(pieRadius, min_creditos > 0 ? Math.round(creditos * pieRadius / min_creditos) : 0);
    const creditosPerc = Math.min(100, min_creditos > 0 ? Math.round(creditos * 100 / min_creditos) : 0);

    return (
      <div id="carreraChart" className="container">
        <div className="row">
          <div className="col-6">
            <svg width="100" height="100">
              <circle style={{ strokeDasharray: `${creditosAng} ${pieRadius}`}} r={radius} cx="50" cy="50" />
            </svg>
            </div>
            <div className="col-6">
              <p className="lead"><strong>{creditosPerc}%</strong> de la carrera aprobada!</p>
              <p>Total: <span className="font-weight-bold text-success">{creditos}</span> / {min_creditos}</p>
            </div>
        </div>
      </div>
    );
  }
}

class MateriasSelect extends React.Component {
  state = {
      data: [],
      isLoading: false,
      placeholder: "Cargando...",
      materiaAction: 'aprobadas',
      materiaEstado: 'A',
      materiaClass: 'funkyradio-success',
      creditos: 0,
      min_creditos: 0,
  };
  constructor(props) {
    super(props);
    this.selectedMaterias = props.materias;
    this.showSaveData = this.showSaveData.bind(this);
  }
  fetchAPI(plancarrera_id) {
    const url = "api/facultad/plancarreras/" + plancarrera_id + "/planmaterias/";

    fetch(url)
      .then((response) => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then((data) => {
        this.setState({ data : data, isLoading: true,
                        min_creditos: this.props.plancarrera.min_creditos });
      })
      .catch(error => this.setState({ placeholder: error, isLoading: false }));
  }
  getDepartamento(id) {
    return id[0] + id[1];
  }
  getCodigo(id) {
    return id[0] + id[1] + '.' + id[2] + id[3];
  }
  isChecked(id) {
    return this.selectedMaterias.has(id);
  }
  /* Actualiza lista de materias y sus estados, y creditos aprobados */
  handleMateriaClick(planmateria, elementId) {
    // Set current class
    document.getElementById(elementId)
            .parentElement.className = this.state.materiaClass;

    const materia = planmateria.materia;

    const { materiaAction, materiaEstado, materiaClass, creditos } = this.state;

    var obj = this.selectedMaterias.get(materia.id);
    if (obj != null) {
      // Substraer creditos aprobados
      if (obj.estado == 'A')
        this.state.creditos -= obj.creditos;
      // Deseleccionar
      if (obj.estado == this.state.materiaEstado)  {
        this.selectedMaterias.delete(materia.id);
      // Cambiar estado
      } else {
        obj.estado = this.state.materiaEstado;
        this.selectedMaterias.set(materia.id, obj);
        // Agregar creditos aprobados
        if (this.state.materiaEstado == 'A')
          this.state.creditos += obj.creditos;
      }
    // Nueva materia
    } else {
      obj = { "materia": materia.id,
              "estado": this.state.materiaEstado,
              "creditos": planmateria.creditos
            };
      this.selectedMaterias.set(materia.id, obj);
      // Agregar creditos aprobados
      if (this.state.materiaEstado == 'A')
        this.state.creditos += obj.creditos;
    }

    this.props.onMateriasChange(this.selectedMaterias);
  }

  updateMateriaAction(materiaAction, materiaEstado, materiaClass) {
    this.setState({ materiaAction: materiaAction,
                    materiaEstado: materiaEstado,
                    materiaClass: materiaClass
                  });
  }
  /* Get descripción del estado */
  getEstado(id) {
    const estados = { 'A': 'Aprobada',
                      'F': 'Final',
                      'C': 'Cursando' }
    const e = this.selectedMaterias.get(id);
    return e ? estados[e] : '';
  }
  showSaveData() {
    this.props.saveData();
    document.getElementById("save-data").className = 'active';
  }
  render() {
    const { data, isLoading, placeholder } = this.state;

    if (!isLoading) return <p>{placeholder}</p>;

    return !data.length ? (
      <p>No hay materias para {this.props.plancarrera.name}</p>
      ) : (
        <React.Fragment>
          <h3 id="elegir-materias-title" className="">Seleccioná tus materias</h3>
          <div className="btn-actions sticky-top">
            <button onClick={(e) => this.updateMateriaAction('aprobadas', 'A', 'funkyradio-success')}
                    className="btn btn-success">Elegir materias aprobadas</button>
            <button onClick={(e) => this.updateMateriaAction('a final', 'F', 'funkyradio-warning')}
                    className="btn btn-warning">Elegir materias a final</button>
            <button onClick={(e) => this.updateMateriaAction('cursando', 'C', 'funkyradio-danger')}
                    className="btn btn-danger">Elegir materias cursando</button>
          </div>
          <div id="materias-list" className="container text-left">
            <div className="funkyradio" id="materias">
              {data.map((el, i, arr) => {
                const prevEl = arr[i - 1];
                return (
                  <React.Fragment key={el.id}>
                    {i == 0 && <div className="cuatrimestre">{el.cuatrimestre}° Cuatrimestre</div>}
                    {i > 0 && el.cuatrimestre != prevEl.cuatrimestre &&
                      (el.cuatrimestre == 99 ?
                        (<div className="cuatrimestre">Electivas</div>)
                        : (<div className="cuatrimestre">{el.cuatrimestre}° Cuatrimestre</div>)
                      )}
                    {el.cuatrimestre == 99 && el.cuatrimestre == prevEl.cuatrimestre &&
                      this.getDepartamento(el.materia.id) != this.getDepartamento(prevEl.materia.id) &&
                      <hr /> }
                    <div className="funkyradio-success">
                      <input type="checkbox" name={`materia${el.id}`}
                          id={`materia${el.id}`}
                          key={uuid()} value={el.id}
                          defaultChecked={this.isChecked(el.materia.id)}
                          onChange={(e) => this.handleMateriaClick(el, `materia${el.id}`)}
                      />
                      <label htmlFor={`materia${el.id}`}>
                        <strong>{this.getCodigo(el.materia.id)}</strong> { el.materia.name }
                        <div id={`estado-${el.id}`} className="float-right">
                          {this.getEstado(el.materia.id)}
                        </div>
                      </label>
                    </div>
                  </React.Fragment>
                );
              })}
            </div>
          </div>
          <CreditosChart creditos={this.state.creditos}
                         min_creditos={this.state.min_creditos}
            />
          <div className="container">
            <button className="account-action-btn btn btn-primary btn-fiubar"
              onClick={this.showSaveData}>Guardar datos</button>
          </div>
      </React.Fragment>
      );
  }
}

class ElegirMaterias extends React.Component {
  constructor(props) {
    super(props);
    this.handleMateriasChange = this.handleMateriasChange.bind(this);
    this.materiasDiv = React.createRef();
  }
  fetchAPI(plancarrera_id) {
    this.materiasDiv.current.fetchAPI(plancarrera_id);
  }
  componentDidUpdate() {
    // document.getElementById('elegir-materias').scrollIntoView({'behavior':'smooth'});
  }
  handleMateriasChange(materias) {
    this.props.onMateriasChange(materias);
  }
  render() {
    return (
      <div id="elegir-materias" className="div-none">
        <hr />
        <h2 className="">{this.props.plancarrera && this.props.plancarrera.name}</h2>
        <MateriasSelect
            ref={this.materiasDiv}
            carrera={this.props.carrera}
            plancarrera={this.props.plancarrera}
            materias={this.props.materias}
            onMateriasChange={this.handleMateriasChange}
            saveData={this.props.saveData}
          />
      </div>
    );
  }
}
export default ElegirMaterias;
