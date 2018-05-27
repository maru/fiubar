import React from "react";
import PropTypes from "prop-types";
import shortid from "shortid";
const uuid = shortid.generate;
const Table = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
    {data.map(el => (
      <img key={el.name} src={`/static/images/facultad/carreras/${el.short_name}.jpg`}
      alt={`${el.name}`} className="" title={`${el.name}`}
      style={{ width: '140px', height: '140px', margin:'5px' }} />
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
