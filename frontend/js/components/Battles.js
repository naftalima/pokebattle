import PropTypes from 'prop-types';
import React from 'react';
import { Link } from 'react-router-dom';

export default function Battles({ battles }) {
  const battleList = battles.map((battle) => {
    return (
      <tr key={battle.id} className="battle-id-btn">
        <Link to={{ pathname: `/v2/battle/${battle.id}` }}>Battle #{battle.id}</Link>
      </tr>
    );
  });
  return (
    <table>
      <td>{battleList}</td>
    </table>
  );
}
Battles.propTypes = {
  battles: PropTypes.array,
};
