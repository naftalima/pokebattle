/* eslint-disable react/prop-types */
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import { getUserName } from '../utils/format';

function BattleTitle({ battleId, creator, opponent }) {
  return (
    <div className="battle-title">
      {battleId === 0 ? (
        <p>there is no battle</p>
      ) : (
        <div>
          <p className="title">Battle #{battleId}</p>
          <h4>
            <span className="trainer">{creator ? getUserName(creator.email) : ''}</span> challenged{' '}
            <span className="trainer">{opponent ? getUserName(opponent.email) : ''}</span>
          </h4>
        </div>
      )}
    </div>
  );
}
BattleTitle.propTypes = {
  battleId: PropTypes.number,
  creator: PropTypes.object,
  opponent: PropTypes.object,
};

const mapStateToProps = (state, ownProps) => {
  const { battles, users } = state.battleR;
  const { battleId } = ownProps;

  const battle = battles[battleId];

  const creatorId = battle ? battle.creator : null;
  const creator = creatorId ? users[creatorId] : {};
  const opponentId = battle ? battle.opponent : null;
  const opponent = opponentId ? users[opponentId] : {};

  return { battleId, creator, opponent };
};

export default connect(mapStateToProps)(BattleTitle);
