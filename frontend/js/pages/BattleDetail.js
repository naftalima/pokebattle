import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';

import BattleTitle from '../components/BattleTitle';
import Team from '../components/Team';
import Winner from '../components/Winner';
import { getBattleDetailAction } from '../redux/actions';

class BattleDetail extends React.Component {
  componentDidMount() {
    const { pathname } = window.location;
    const battleId = Number(pathname.split('/').pop());

    const { fetchBattle } = this.props;
    fetchBattle(battleId);
  }

  render() {
    const { battle } = this.props;

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
            <Winner battleId={battle.id} />
          </div>
        </div>
      </div>
    );
  }
}
BattleDetail.propTypes = {
  fetchBattle: PropTypes.func,
  battle: PropTypes.object,
};

const mapStateToProps = (state) => {
  const { battles } = state.battleR;

  const { pathname } = window.location;
  const battleId = Number(pathname.split('/').pop());

  const battle = battles[battleId] ? battles[battleId] : {};

  return { battle };
};

const mapDispatchToProps = (dispatch) => {
  return {
    fetchBattle: (id) => dispatch(getBattleDetailAction(id)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(BattleDetail);
