import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';

import BattleTitle from '../components/BattleTitle';
import Loading from '../components/Loading';
import Team from '../components/Team';
import Winner from '../components/Winner';
import { getBattleDetailAction } from '../redux/actions';

function BattleDetail(props) {
  const { fetchBattle, battle, emptyBattle } = props;
  const { id } = useParams();
  console.log(id);

  useEffect(() => {
    if (battle && battle.id !== Number(id)) {
      fetchBattle(id);
    }
  });

  if (emptyBattle) {
    return <Loading />;
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
  emptyBattle: PropTypes.bool,
};

const mapStateToProps = (state, ownProps) => {
  const { battles } = state.battleR;
  const {
    match: { params },
  } = ownProps;
  const battleId = params ? params.id : {};

  const emptyBattles = Object.keys(battles).length === 0 && battles.constructor === Object;
  const battle = !emptyBattles ? battles[battleId] : {};
  const emptyBattle = Object.keys(battle).length === 0 && battle.constructor === Object;
  return { battle, emptyBattle };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchBattle: (id) => dispatch(getBattleDetailAction(id)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
