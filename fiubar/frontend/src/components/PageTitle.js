import React from "react";

class PageTitle extends React.Component {
  render() {
    return (
      <div id="head-title">
        <h1 className="cover-heading">Fiubar</h1>
        <p>
          Administrador de materias para <a href="http://www.fi.uba.ar/" className="fiuba-link">FIUBA</a>
        </p>
      </div>
    );
  }
}
export default PageTitle;
