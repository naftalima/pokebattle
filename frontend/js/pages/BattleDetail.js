import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router';

import BattleTitle from '../components/BattleTitle';
import Team from '../components/Team';
import Winner from '../components/Winner';
import { getBattleDetailAction } from '../redux/actions';

function BattleDetail(props) {
  const {
    match: { params },
    fetchBattle,
    battle,
  } = props;
  const battleId = params.id;

  useEffect(() => {
    if (battle && battle.id !== Number(battleId)) {
      fetchBattle(battleId);
    }
  });

  if (!battle.id) {
    return (
      <div className="container">
        <div className="battleDetail">
          <h1>Its not a valid battle id</h1>
        </div>
      </div>
    );
  }

  const battleTeam = battle ? battle.teams : [null, null];
  const [creatorTeamId, opponentTeamId] = battleTeam;

  return (
    <div className="container">
      <div className="battleDetail">
        <div className="battleDetail">
          <BattleTitle battleId={battle.id} />
          <Team trainerTeamId={creatorTeamId} />
          <Team trainerTeamId={opponentTeamId} />
          <Winner winnerId={battle.winner} />
        </div>
      </div>
    </div>
  );
}
BattleDetail.propTypes = {
  fetchBattle: PropTypes.func,
  battle: PropTypes.object,
  match: PropTypes.object,
};

const mapStateToProps = (state, ownProps) => {
  const { battles } = state.battleR;
  const {
    match: { params },
  } = ownProps;
  const battleId = params.id;

  const battle = battles[battleId] ? battles[battleId] : {};

  return { battle };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchBattle: (id) => dispatch(getBattleDetailAction(id)),
  };
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(BattleDetail));
