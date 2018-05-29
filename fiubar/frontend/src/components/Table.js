import React from "react";
import PropTypes from "prop-types";

const Table = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="container">
    {data.map(el => (
        <div className="box text-center" key={el.short_name}
            style={{ background: `linear-gradient(
                                    rgba(0, 0, 0, 0.5),
                                    rgba(0, 0, 0, 0.5)
                                  ), url(/static/images/facultad/carreras/${el.short_name}.jpg)  no-repeat center center`
                  }}

            >
            <div>{el.name}</div>
        </div>
    ))}
    </div>
  );
  //     <h2 className="subtitle">
  //       Showing <strong>{data.length} items</strong>
  //     </h2>
  //     <table className="table materias-list table-hover table-condensed table-striped">
  //       <thead>
  //         <tr>
  //           {Object.entries(data[0]).map(el => <th key={uuid()}>{el[0]}</th>)}
  //         </tr>
  //       </thead>
  //       <tbody>
  //         {data.map(el => (
  //           <tr key={el.id}>
  //             {Object.entries(el).map(el => <td key={uuid()}>{el[1]}</td>)}
  //           </tr>
  //         ))}
  //       </tbody>
  //     </table>
  //   </div>
  // );
Table.propTypes = {
  data: PropTypes.array.isRequired
};
export default Table;
