/* eslint-disable react/prop-types */
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getUserName } from '../utils/format';

function Winner({ winner }) {
  return (
    <div className="winner">
      {!winner ? (
        <h2>There is no winner yet</h2>
      ) : (
        <h2>
          And the winner is <span className="winner">{getUserName(winner.email)}</span>
        </h2>
      )}
    </div>
  );
}
Winner.propTypes = {
  winner: PropTypes.object,
};

const mapStateToProps = (state, ownProps) => {
  const { users } = state.battleR;
  const { winnerId } = ownProps;

  const winner = winnerId ? users[winnerId] : null;
  return { winner };
};

export default connect(mapStateToProps)(Winner);
