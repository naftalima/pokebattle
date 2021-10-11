import PropTypes from 'prop-types';
import React from 'react';
import { Link } from 'react-router-dom';

export default function Battles({ battles }) {
  return (
    <table>
      <td>
        {battles.map((battle) => (
          <tr key={battle.id} className="battle-id-btn">
            <Link to={{ pathname: `/v2/battle/${battle.id}` }}>Battle #{battle.id}</Link>
          </tr>
        ))}
      </td>
    </table>
  );
}
Battles.propTypes = {
  battles: PropTypes.array,
};
