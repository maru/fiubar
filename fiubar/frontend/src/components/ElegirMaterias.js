import React from "react";
import shortid from "shortid";

const uuid = shortid.generate;

class MateriasSelect extends React.Component {
  state = {
      data: [],
      isLoading: false,
      placeholder: "Cargando...",
      materiaAction: 'aprobadas',
      materiaEstado: 'A',
      materiaClass: 'funkyradio-success',
  };
  constructor(props) {
    super(props);
    this.selectedMaterias = props.materias;
  }
  fetchAPI(plancarrera_id) {
    const url = "api/facultad/plancarreras/" + plancarrera_id + "/planmaterias/";

    fetch(url)

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
  getDepartamento(id) {
    return id[0] + id[1];
  }
  getCodigo(id) {
    return id[0] + id[1] + '.' + id[2] + id[3];
  }
  isChecked(id) {
    return this.selectedMaterias.has(id);
  }
  handleMateriaClick(planmateria, elementId) {
    // Set current class
    document.getElementById(elementId)
            .parentElement.className = this.state.materiaClass;

    const materia = planmateria.materia;

    var obj = this.selectedMaterias.get(materia.id);
    if (obj != null) {
      // Deseleccionar
      if (obj.estado == this.state.materiaEstado)  {
        this.selectedMaterias.delete(materia.id);
      // Cambiar estado
      } else {
        obj.estado = this.state.materiaEstado;
        this.selectedMaterias.set(materia.id, obj);
      }
    // Nueva materia
    } else {
      obj = { "materia": materia.id,
              "estado": this.state.materiaEstado,
              "creditos": planmateria.creditos
            };
      this.selectedMaterias.set(materia.id, obj);
    }
    this.props.onMateriasChange(this.selectedMaterias);
  }
  updateMateriaAction(materiaAction, materiaEstado, materiaClass) {
    var m = document.getElementById('materias');
    for (var i = 0; i < m.childElementCount; i++) {
      if (m.children[i].childElementCount == 0 ||
          m.children[i].children[0].tagName != 'INPUT' ||
          m.children[i].children[0].checked) continue;
      m.children[i].className = materiaClass;
    }
    this.setState({ materiaAction: materiaAction,
                    materiaEstado: materiaEstado,
                    materiaClass: materiaClass
                  });
  }
  getEstado(id) {
    const estados = { 'A': 'Aprobada',
                      'F': 'Final',
                      'C': 'Cursando' }
    if (this.selectedMaterias.has(id)) {
      const e = this.selectedMaterias.get(id);
      return estados[e];
    }
  }
  render() {
    const { data, isLoading, placeholder } = this.state;

    if (!isLoading) return <p>{placeholder}</p>;

    return !data.length ? (
      <p>No hay materias para {this.props.plancarrera.name}</p>
      ) : (
        <React.Fragment>
          <h3 id="elegir-materias-title" className="">Seleccioná tus materias</h3>
          <div className="btn-actions">
            <button onClick={(e) => this.updateMateriaAction('aprobadas', 'A', 'funkyradio-success')}
                    className="btn btn-success">Elegir materias aprobadas</button>
            <button onClick={(e) => this.updateMateriaAction('a final', 'F', 'funkyradio-warning')}
                    className="btn btn-warning">Elegir materias a final</button>
            <button onClick={(e) => this.updateMateriaAction('cursando', 'C', 'funkyradio-danger')}
                    className="btn btn-danger">Elegir materias cursando</button>
          </div>
          <div className="container text-left">
            <form>
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
            </form>
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
          />
      </div>
    );
  }
}
export default ElegirMaterias;
